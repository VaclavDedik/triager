import os
import shutil
import joblib

import models

from classifier import tests
from classifier.document import Document
from flask import render_template, flash, redirect, url_for

from triager import app, db
from models import Project
from forms import ProjectForm, IssueForm, DataSourceForm


@app.route("/")
def homepage():
    projects = db.session.query(Project.id, Project.name)
    return render_template("index.html", projects=projects)


@app.route("/project/<id>", methods=['GET', 'POST'])
def view_project(id):
    project = Project.query.get_or_404(id)

    form = IssueForm()
    predictions = []

    if form.validate_on_submit():
        issue = Document(form.summary.data, form.description.data)
        model = joblib.load(
            os.path.join(app.config['MODEL_FOLDER'], '%s/svm.pkl' % id))
        try:
            predictions = model.predict(issue, n=10)
        except ValueError:
            flash("There is too little information provided. "
                  "You need to add more text to the description or summary.",
                  "error")

    fscore = tests.fscore(project.precision, project.recall)
    return render_template("project/view.html", project=project, fscore=fscore,
                           form=form, predictions=predictions)


@app.route("/project/create", methods=['GET', 'POST'])
def create_project():
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


#
# Context Processors
#
@app.context_processor
def all_projects():
    projects = db.session.query(Project.id, Project.name)
    return dict(all_projects=projects)
