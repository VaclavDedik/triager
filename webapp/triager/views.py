import models

from flask import render_template, flash, redirect, url_for

from triager import app, db
from models import Project
from forms import ProjectForm, IssueForm, DataSourceForm


@app.route("/")
def homepage():
    projects = Project.query
    return render_template("index.html", projects=projects)


@app.route("/project/<id>")
def view_project(id):
    project = Project.query.get_or_404(id)
    return render_template("project/view.html", project=project)


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


@app.route("/project/<id>/triage", methods=['GET', 'POST'])
def triage_project(id):
    project = Project.query.get_or_404(id)
    form = IssueForm()

    return render_template("project/triage.html",
                           form=form, project=project)


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
            flash("Project %s sucessfully updated." % project.name)
            return redirect(url_for('view_project', id=project.id))

    return render_template("project/edit.html",
                           form=form, ds_forms=ds_forms, project=project)


# Context Processors
@app.context_processor
def all_projects():
    projects = Project.query
    return dict(all_projects=projects)