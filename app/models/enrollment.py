from app.models.base import db
import sqlalchemy_utils as su


@su.generic_repr
class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer(), db.ForeignKey("course.id"))
