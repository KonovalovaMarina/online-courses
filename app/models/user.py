import enum

from flask_login import UserMixin
import sqlalchemy_utils as su

from .base import db


class UserRole(enum.Enum):
    student = "student"
    admin = "admin"


@su.generic_repr
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    login = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(su.PasswordType(schemes=["pbkdf2_sha512"]), nullable=True)
    role = db.Column(su.ChoiceType(UserRole, db.String(10)), default=UserRole.student, nullable=False)

    def is_admin(self):
        return self.role == UserRole.admin

    def is_student(self):
        return self.role == UserRole.student
