import os
import shutil
import joblib

import models

from classifier import tests
from classifier.document import Document
from flask import render_template, flash, redirect, url_for
from flask import jsonify, make_response, request
from flask.ext.login import login_user, login_required, logout_user

from triager import app, db, config
from models import Project, TrainStatus as TS, Feedback
from forms import ProjectForm, IssueForm, DataSourceForm, ConfigurationForm
from forms import LoginForm, FeedbackForm
from auth import User
from utils import hash_pwd


@app.route("/")
def homepage():
    projects = Project.query
    return render_template("index.html", projects=projects)


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = ConfigurationForm(obj=config)

    if form.validate_on_submit():
        # auth__admin is special, because it needs to be hashed before being
        # passed to the config and saved
        auth__admin = form.auth__admin.data
        form.auth__admin.data = None
        form.populate_obj(config)
        if auth__admin:
            config.auth__admin = hash_pwd(auth__admin)

        config.save()
        flash("Settings successfully updated")
        return redirect(url_for("settings"))

    # No need to present a hash digest to the user :)
    form.auth__admin.data = None

    return render_template("settings.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        login_user(user)

        flash('Logged in successfully.')
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('homepage'))


@app.route("/project/<id>", methods=['GET', 'POST'])
def view_project(id):
    project = Project.query.get_or_404(id)

    form = IssueForm()
    feedback_form = FeedbackForm()
    predictions = []
    model_path = os.path.join(app.config['MODEL_FOLDER'], '%s/svm.pkl' % id)
    trained = project.train_status != TS.NOT_TRAINED \
        and os.path.isfile(model_path)
    summary_or_description = form.summary.data or form.description.data

    if trained and form.validate_on_submit() and summary_or_description:
        issue = Document(form.summary.data, form.description.data)
        model = joblib.load(model_path)
        try:
            predictions = model.predict(issue, n=10)
        except ValueError:
            flash("There is too little information provided. "
                  "You need to add more text to the description or summary.",
                  "error")

        feedback_form.summary.data = form.summary.data
        feedback_form.description.data = form.description.data
        existing_feedback = Feedback.query.get(
            Feedback.get_id_from_doc(issue, project=project))
        if existing_feedback:
            feedback_form.confirmed_recommendation.data = \
                existing_feedback.confirmed_recommendation

    if request.method == "POST" and not summary_or_description:
        err_msg = "Summary or description must not be empty."
        form.summary.errors.append(err_msg)
        form.description.errors.append(err_msg)

    fscore = tests.fscore(project.precision, project.recall)
    return render_template("project/view.html", project=project, fscore=fscore,
                           form=form, predictions=predictions, trained=trained,
                           feedback_form=feedback_form)


@app.route("/project/create", methods=['GET', 'POST'])
@login_required
def create_project():
    config.reload()
    form = ProjectForm()
    ds_forms = dict([
        (cls.populates, cls()) for cls in DataSourceForm.__subclasses__()])

    form.datasource_type.choices = [
        (cls.populates, cls.name) for cls in DataSourceForm.__subclasses__()]
    form.datasource_type.choices.insert(0, (None, "-- Select Data Source --"))
    new_project = Project()

    if form.validate_on_submit():
        form.populate_obj(new_project)
        ds_form = ds_forms[form.datasource_type.data]

        if ds_form.validate():
            new_project.datasource = \
                getattr(models, form.datasource_type.data)()
            ds_form.populate_obj(new_project.datasource)

            db.session.add(new_project)
            db.session.commit()
            flash("New project successfully created.")
            return redirect(url_for('view_project', id=new_project.id))

    return render_template("project/create.html",
                           form=form, ds_forms=ds_forms, project=new_project)


@app.route("/project/<id>/edit", methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    ds_forms = dict([
        (cls.populates, cls()) for cls in DataSourceForm.__subclasses__()])
    for populates, ds_form in ds_forms.items():
        if populates == project.datasource.__class__.__name__:
            ds_forms[populates] = ds_form.__class__(obj=project.datasource)
            current_ds_type = populates

    form = ProjectForm(obj=project, datasource_type=current_ds_type)
    form.datasource_type.choices = [
        (cls.populates, cls.name) for cls in DataSourceForm.__subclasses__()]
    form.datasource_type.choices.insert(0, (None, "-- Select Data Source --"))

    if form.validate_on_submit():
        form.populate_obj(project)
        ds_form = ds_forms[form.datasource_type.data]

        if ds_form.validate():
            project.datasource = getattr(models, form.datasource_type.data)()
            ds_form.populate_obj(project.datasource)

            db.session.add(project)
            db.session.commit()
            flash("Project %s successfully updated." % project.name)
            return redirect(url_for('view_project', id=project.id))

    return render_template("project/edit.html",
                           form=form, ds_forms=ds_forms, project=project)


@app.route("/project/<id>/delete", methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)

    # Delete project form database
    db.session.delete(project)
    db.session.commit()

    # Remove model data
    model_dir = os.path.join(app.config['MODEL_FOLDER'], str(id))
    shutil.rmtree(model_dir, ignore_errors=True)

    flash("Project %s successfully deleted." % project.name)
    return redirect(url_for('homepage'))


@app.route("/project/<id>/feedback", methods=['POST'])
def post_feedback(id):
    project = Project.query.get_or_404(id)

    form = FeedbackForm()
    if form.validate():
        issue = Document(form.summary.data, form.description.data)
        feedback = Feedback()
        feedback.project = project
        feedback.id = Feedback.get_id_from_doc(issue, project=project)
        existing_feedback = Feedback.query.get(feedback.id)
        if existing_feedback:
            feedback = existing_feedback

        if form.selected_recommendation.data:
            feedback.selected_recommendation = \
                form.selected_recommendation.data
        if form.confirmed_recommendation.data:
            feedback.confirmed_recommendation = \
                form.confirmed_recommendation.data
        db.session.add(feedback)
        db.session.commit()

        return jsonify(result="success")

    return jsonify(result="error", errors=form.errors), 400

@app.route("/feedback.csv")
def feedback_csv():
    all_feedback = Feedback.query
    csv_vals = "project_id,selected,confirmed,accuracy,precision,recall\n"
    for feedback in all_feedback:
        csv_vals += "%s,%s,%s,%4.4f,%4.4f,%4.4f\n" \
            % (feedback.project.id, feedback.selected_recommendation,
               feedback.confirmed_recommendation, feedback.project.accuracy,
               feedback.project.precision, feedback.project.recall)

    resp = make_response(csv_vals)
    if request.args.get("plain"):
        resp.mimetype = "text/plain"
    else:
        resp.mimetype = "text/csv"

    return resp


#
# Context Processors
#
@app.context_processor
def all_projects():
    projects = db.session.query(Project.id, Project.name)
    return dict(all_projects=projects)


@app.context_processor
def scheduler_running_check():
    result = dict(is_scheduler_running=False)
    scheduler_pid_file = app.config['SCHEDULER_PID_FILE']

    if os.path.isfile(scheduler_pid_file):
        with open(scheduler_pid_file, 'r') as f:
            scheduler_pid = int(f.read())
        try:
            os.kill(scheduler_pid, 0)
            result['is_scheduler_running'] = True
        except OSError:
            # Scheduler not running
            pass

    return result
