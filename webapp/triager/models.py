from triager import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #: Name of the project
    name = db.Column(db.String(63), nullable=False)
