from app.models.base import db
import sqlalchemy_utils as su
import sqlalchemy.orm as so
from .course import Course
from .user import User


@su.generic_repr
class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    course_id = db.Column(db.Integer(), db.ForeignKey(Course.id))

    course = so.relationship(Course, backref=so.backref("enrollments", cascade="all,delete-orphan"))
    user = so.relationship(User, backref=so.backref("enrollments", cascade="all,delete-orphan"))
