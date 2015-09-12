import re
import hashlib

from classifier.document import Document

from triager import db, config
from jira import Jira


class TrainStatus(object):
    NOT_TRAINED = "not_trained"
    QUEUED = "queued"
    TRAINING = "training"
    TRAINED = "trained"
    FAILED = "failed"

    @classmethod
    def is_active(cls, status):
        active_statuses = [cls.TRAINING, cls.FAILED, cls.QUEUED]
        return status in active_statuses


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #: Name of the project
    name = db.Column(db.String(63), nullable=False)

    datasource_id = db.Column(db.Integer, db.ForeignKey('datasource.id'))
    datasource = db.relationship("DataSource")

    train_status = db.Column(
        db.String(10), default=TrainStatus.NOT_TRAINED, nullable=False)
    training_message = db.Column(db.String(253))
    schedule = db.Column(db.String(63), default="0 0 * * *")
    last_training = db.Column(db.Float(), default=0.0)

    accuracy = db.Column(db.Float(), default=0.0)
    precision = db.Column(db.Float(), default=0.0)
    recall = db.Column(db.Float(), default=0.0)

    __table_args__ = {'sqlite_autoincrement': True}


class Feedback(db.Model):
    id = db.Column(db.String(128), primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship("Project")

    selected_recommendation = db.Column(db.Integer, default=0)
    confirmed_recommendation = db.Column(db.Integer, default=0)

    @classmethod
    def get_id_from_doc(cls, document, project=None):
        title = document.title if document.title else ""
        content = document.content if document.content else ""
        project_id = str(project.id) if project else ""

        striped_doc = re.sub(r'\s+', '', project_id + title + content)
        digest = hashlib.sha512(striped_doc).hexdigest()

        return digest


class DataSource(db.Model):
    __tablename__ = "datasource"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def get_data(self):
        raise NotImplementedError()


class JiraDataSource(DataSource):
    jira_api_url = db.Column(db.String(253))
    jira_project_key = db.Column(db.String(63))
    jira_statuses = db.Column(db.String(63), default="Resolved,Closed")
    jira_resolutions = db.Column(db.String(63), default="Fixed")

    __mapper_args__ = {
        'polymorphic_identity': 'jira'
    }

    def get_data(self):
        jira = Jira(self.jira_api_url)
        jql = "project=%s and status in (%s) " + \
              "and resolution in (%s) and assignee!=null"
        jql = jql % (self.jira_project_key, self.jira_statuses,
                     self.jira_resolutions)
        fields = 'summary,description,assignee,created'
        raw_issues = jira.find_all(jql, fields,
                                   limit=int(config.general__ticket_limit))

        data = []
        for issue in raw_issues:
            fields = issue['fields']
            document = Document(fields['summary'], fields['description'],
                                fields['assignee']['name'])
            data.append(document)

        return data
