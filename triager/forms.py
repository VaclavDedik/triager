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
from triager import jira


#
# Validators
#
def validate_cron_format(form, field):
    try:
        croniter(field.data, time.time())
    except Exception:
        raise ValidationError('Training Schedule must be in a CRON format.')


def validate_jira_url(form, field):
    try:
        jira_ = jira.Jira(field.data)
        jira_.test_jira_availability()
    except Exception as ex:
        raise ValidationError('Invalid Jira URL: %s' % ex.message)


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
        'Data Source Type',
        description="Choose datasource type that will be used to retrieve "
                    "the data for training."
    )

    schedule = StringField(
        'Training Schedule',
        validators=[
            DataRequired(),
            validate_cron_format
        ],
        default=lambda: config.defaults__schedule,
        description="Specify how often you want the project to be retrained. "
                    "If you choose to retrain the project model often, "
                    "Triager is less likely to base its recommendation on "
                    "old data. On the other hand, training can take a lot of "
                    "hardware resources in that case. It is very likely that "
                    "it is sufficient for your project to be trained every "
                    "week and that is therefore the recommended value. Use "
                    "CRON format, see: "
                    "'http://www.nncron.ru/help/EN/working/cron-format.htm'."
    )


class DataSourceForm(Form):
    pass


class JiraDataSourceForm(DataSourceForm):
    populates = "JiraDataSource"
    name = "Jira Data Source"

    jira_api_url = StringField(
        'Jira API URL',
        validators=[
            DataRequired(),
            URL(),
            validate_jira_url
        ],
        description="URL of the rest API of your Jira instance. It is usually "
                    "something similar to "
                    "'http://jira.example.com/rest/api/latest/'."
    )

    jira_project_key = StringField(
        'Project key',
        validators=[DataRequired()],
        description="Project key is a short unique identification of a "
                    "project in Jira. When you are viewing an issue that "
                    "belongs to the desired project, the URL usually looks "
                    "something like this: "
                    "'http://jira.example.com/browse/PROJ-10'. Project key in "
                    "this case is 'PROJ'."
    )

    jira_statuses = StringField(
        'Statuses',
        validators=[DataRequired()],
        default=lambda: config.jira__default_statuses,
        description="Pay a lot of attention to this field. This field should "
                    "list all Jira statuses that a finished issue can be in. "
                    "Separate multiple statuses by commas. The value of this "
                    "field is usually 'Resolved' and 'Closed'. It can, "
                    "however, be something else if you configured your Jira "
                    "differently. Never fill in values that do not exist in "
                    "your Jira, otherwise you will get an error."
    )

    jira_resolutions = StringField(
        'Resolutions',
        default=lambda: config.jira__default_resolutions,
        description="Pay a lot of attention to this field. This field should "
                    "list all Jira resolutions that a fixed issue can be in. "
                    "It should not include resolutions like 'Wontfix' or "
                    "'Duplicate'. It should usually be something like 'Fixed' "
                    "or 'Done'. You can separate multiple resolutions by "
                    "commas. Never fill in values that do not exist in your "
                    "Jira, otherwise you will get an error."
    )


class IssueForm(Form):
    summary = StringField(
        'Summary'
    )

    description = StringField(
        'Description',
        widget=TextArea()
    )


class FeedbackForm(IssueForm):
    selected_recommendation = IntegerField(default=0)
    confirmed_recommendation = IntegerField(default=0)


class ConfigurationForm(Form):
    general__ticket_limit = IntegerField(
        'Ticket limit',
        validators=[
            InputRequired(),
            NumberRange(min=1000)
        ],
        description="Maximum number of tickets/issues/bugs that the "
                    "Triager will use for training. The higher the limit, "
                    "the more accurate will the Triager possibly be. This is, "
                    "however, not certain. On the other hand, the lower the "
                    "limit, the less time it will take to train the Triager. "
                    "It is reasonable to use a value somewhat between 1000 "
                    "and 10000. Be aware that anything beyond 10000 could "
                    "take days to train."
    )

    general__min_class_occur = IntegerField(
        'Minimum number of classes',
        validators=[
            InputRequired(),
            NumberRange(min=3)
        ],
        description="For better performance, some developers are removed from "
                    "the training datasets and are therefore not considered "
                    "for recommendation. The removed developers are in this "
                    "case those that did not fix at least a certain number of "
                    "bug reports. The number of such tickets can be tuned by "
                    "modifying this value. You should usually choose "
                    "something like 1 percent of the ticket limit value. So "
                    "if you chose 2000 for ticket limit, this value should be "
                    "about 20. Be aware that to tune this parameter can be "
                    "rather tricky. You also should not usually go beyond "
                    "value of about 50. I recommend to use 1 percent for "
                    "ticket limit values of 1000-3000, and 30 for anything "
                    "beyond ticket limit value of 3000."
    )

    auth__admin = StringField(
        'New admin password',
        description="New password for admin. If no value is filled in, the "
                    "password remains unchanged."
    )

    defaults__schedule = StringField(
        'Schedule',
        validators=[
            DataRequired(),
            validate_cron_format
        ],
        description="Default schedule value that will be used to prefill "
                    "the schedule field when creating new projects."
    )

    svm__coefficient = FloatField(
        'SVM coefficient (C parameter)',
        validators=[
            InputRequired(),
            NumberRange(min=0.0)
        ],
        description="SVM regularization parameter (C). You should not touch "
                    "this unless you are really sure what you are doing."
    )

    svm__cache_size = IntegerField(
        'SVM cache limit',
        validators=[
            InputRequired(),
            NumberRange(min=100)
        ],
        description="SVM cache limit im MB. The higher the value, the more "
                    "memory will Triager require to train projects."
    )

    jira__default_statuses = StringField(
        'Default statuses',
        validators=[DataRequired()],
        description="Default statuses value that will be used to prefill "
                    "the statuses field when creating new projects."
    )

    jira__default_resolutions = StringField(
        'Default resolutions',
        description="Default resolutions value that will be used to prefill "
                    "the resolutions field when creating new projects."
    )
