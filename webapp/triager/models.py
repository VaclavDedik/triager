import parsers

from triager import db


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


class DataSource(db.Model):
    __tablename__ = "datasource"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(63))

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def get_data(self):
        raise NotImplementedError()


class BugzillaDataSource(DataSource):
    bz_filepath = db.Column(db.String(1023))

    __mapper_args__ = {
        'polymorphic_identity': 'bugzilla'
    }

    def get_data(self):
        parser = parsers.BugzillaParser(folder=self.bz_filepath)
        return parser.parse()


class MRSDataSource(DataSource):
    mrs_filepath = db.Column(db.String(1023))

    __mapper_args__ = {
        'polymorphic_identity': 'mrs'
    }

    def get_data(self):
        parser = parsers.MRSParser(folder=self.mrs_filepath)
        return parser.parse()
