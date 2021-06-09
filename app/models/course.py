from app.models.base import db
import sqlalchemy_utils as su


@su.generic_repr
class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    is_started = db.Column(db.Boolean(), default=False)
