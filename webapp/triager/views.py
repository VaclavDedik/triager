from flask import render_template, flash, redirect, url_for

from triager import app, db
from models import Project
from forms import ProjectForm, IssueForm


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/project/<id>")
def view_project(id):
    project = Project.query.get_or_404(id)
    return render_template("project/view.html", project=project)


@app.route("/project/create", methods=['GET', 'POST'])
def create_project():
    form = ProjectForm()
    new_project = Project()

    if form.validate_on_submit():
        form.populate_obj(new_project)
        db.session.add(new_project)
        db.session.commit()
        flash("New project successfully created.")
        return redirect(url_for('view_project', id=new_project.id))

    return render_template("project/create.html",
                           form=form, project=new_project)


@app.route("/projects")
def list_projects():
    projects = Project.query
    return render_template("project/list.html", projects=projects)


@app.route("/project/<id>/triage", methods=['GET', 'POST'])
def triage_project(id):
    project = Project.query.get_or_404(id)
    form = IssueForm()

    return render_template("project/triage.html",
                           form=form, project=project)


@app.route("/project/<id>/edit", methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.add(project)
        db.session.commit()
        flash("Project %s sucessfully updated." % project.name)
        return redirect(url_for('view_project', id=project.id))

    return render_template("project/edit.html",
                           form=form, project=project)


# Context Processors
@app.context_processor
def all_projects():
    projects = Project.query
    return dict(all_projects=projects)
