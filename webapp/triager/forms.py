from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class ProjectForm(Form):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=4, max=50)
        ]
    )


class IssueForm(Form):
    summary = StringField(
        'Summary'
    )

    description = StringField(
        'Description',
        widget=TextArea()
    )
