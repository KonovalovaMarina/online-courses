from .base import db
import sqlalchemy_utils as su


@su.generic_repr
class Module(db.Model):
    __tablename__ = "module"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey("course.id"))
    deadline = db.Column(db.DateTime())
