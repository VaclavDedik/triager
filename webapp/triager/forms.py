from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ProjectForm(Form):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=4, max=50)
        ]
    )
