import parsers

from triager import db


class TrainStatus(object):
    NOT_TRAINED = "not_trained"
    TRAINING = "training"
    TRAINED = "trained"
    FAILED = "failed"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #: Name of the project
    name = db.Column(db.String(63), nullable=False)

    datasource_id = db.Column(db.Integer, db.ForeignKey('datasource.id'))
    datasource = db.relationship("DataSource")

    train_status = db.Column(
        db.String(10), default=TrainStatus.NOT_TRAINED, nullable=False)


class DataSource(db.Model):
    __tablename__ = "datasource"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type
    }


class BugzillaDataSource(DataSource):
    filepath = db.Column(db.String(1023), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'bugzilla'
    }

    def get_data(self):
        parser = parsers.BugzillaParser(folder=self.filepath)
        return parser.parse()
