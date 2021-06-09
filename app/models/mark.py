from .base import db
import sqlalchemy_utils as su


@su.generic_repr
class Mark(db.Model):
    __tablename__ = "mark"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    module_id = db.Column(db.Integer(), db.ForeignKey("module.id"))
    mark = db.Column(db.Integer(), nullable=False)
