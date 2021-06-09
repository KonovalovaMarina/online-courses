from .course import Course
from .base import db
import sqlalchemy_utils as su
import sqlalchemy.orm as so


@su.generic_repr
class Lecture(db.Model):
    __tablename__ = "lecture"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    ref = db.Column(db.String(), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey(Course.id))

    course = so.relationship(Course, backref=so.backref("lectures", cascade="all,delete-orphan"))

