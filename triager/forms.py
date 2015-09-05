import time

from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, FloatField
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, URL
from wtforms.validators import ValidationError, InputRequired
from wtforms.widgets import TextArea
from croniter import croniter

from triager import config
from triager import auth


#
# Validators
#
def validate_cron_format(form, field):
    try:
        croniter(field.data, time.time())
    except Exception:
        raise ValidationError('Training Schedule must be in a CRON format.')


#
# Forms
#
class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            auth.validate_password
        ]
    )


class ProjectForm(Form):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
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
        default=config.defaults__schedule
    )


class DataSourceForm(Form):
    pass


class BugzillaDataSourceForm(DataSourceForm):
    populates = "BugzillaDataSource"
    name = "Bugzilla Data Source"

    bz_filepath = StringField(
        'File Path',
        validators=[
            DataRequired(),
            Length(max=1023)
        ]
    )


class MRSDataSourceForm(DataSourceForm):
    populates = "MRSDataSource"
    name = "MRS Data Source"

    mrs_filepath = StringField(
        'File Path',
        validators=[
            DataRequired(),
            Length(max=1023)
        ]
    )


class JiraDataSourceForm(DataSourceForm):
    populates = "JiraDataSource"
    name = "Jira Data Source"

    jira_api_url = StringField(
        'Jira API URL',
        validators=[
            DataRequired(),
            URL()
        ]
    )

    jira_project_key = StringField(
        'Project key',
        validators=[DataRequired()]
    )

    jira_statuses = StringField(
        'Statuses',
        validators=[DataRequired()],
        default=config.jira__default_status
    )

    jira_resolutions = StringField(
        'Resolutions',
        validators=[DataRequired()],
        default=config.jira__default_resolutions
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


class ConfigurationForm(Form):
    general__ticket_limit = IntegerField(
        'Ticket limit',
        validators=[
            InputRequired(),
            NumberRange(min=1000)
        ]
    )

    general__min_class_occur = IntegerField(
        'Minimum number of classes',
        validators=[
            InputRequired(),
            NumberRange(min=3)
        ]
    )

    defaults__schedule = StringField(
        'Schedule',
        validators=[
            DataRequired(),
            validate_cron_format
        ]
    )

    svm__coefficient = FloatField(
        'SVM coefficient (C parameter)',
        validators=[
            InputRequired(),
            NumberRange(min=0.0)
        ]
    )

    svm__cache_size = IntegerField(
        'SVM cache limit',
        validators=[
            InputRequired(),
            NumberRange(min=100)
        ]
    )

    jira__default_status = StringField(
        'Default statuses',
        validators=[DataRequired()]
    )

    jira__default_resolutions = StringField(
        'Default resolutions',
        validators=[DataRequired()]
    )

    auth__admin = StringField(
        'Admin password',
        validators=[DataRequired()]
    )
