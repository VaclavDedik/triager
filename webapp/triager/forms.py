import time

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import TextArea
from wtforms.fields import SelectField
from croniter import croniter


#
# Validators
#
def validate_cron_format(form, field):
    try:
        croniter(field.data, time.time())
    except Exception as ex:
        raise ValidationError('Training Schedule must be in a CRON format.')


#
# Forms
#
class ProjectForm(Form):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=4, max=50)
        ]
    )

    datasource_type = SelectField(
        'Data Source Type'
    )

    schedule = StringField(
        'Training Schedule',
        validators=[
            DataRequired(),
            validate_cron_format
        ],
        default="0 0 * * *"
    )


class DataSourceForm(Form):
    pass


class BugzillaDataSourceForm(DataSourceForm):
    populates = "BugzillaDataSource"
    name = "Bugzilla Data Source"

    filepath = StringField(
        'File Path',
        validators=[
            DataRequired(),
            Length(max=1023)
        ]
    )


class IssueForm(Form):
    summary = StringField(
        'Summary',
        validators=[DataRequired()]
    )

    description = StringField(
        'Description',
        widget=TextArea()
    )
