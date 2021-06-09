import enum
import uuid
from datetime import datetime
from urllib.parse import urljoin

from flask import url_for

from .base import db
from .lecture import Lecture
from .user import User
from sqlalchemy_media import File
import sqlalchemy_utils as su
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID

from .. import settings


@su.generic_repr
class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    lecture_id = db.Column(db.Integer(), db.ForeignKey(Lecture.id))
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)

    lecture = so.relationship(Lecture, backref=so.backref("tasks", cascade="all,delete-orphan"))


class SolutionFile(File):
    __directory__ = "solutions"


class SolutionLogsFile(File):
    __directory__ = "logs"


@su.generic_repr
class TaskSolution(db.Model):
    __tablename__ = "task_solution"

    class Status(enum.Enum):
        new = 'new'
        testing = 'testing'
        done = 'done'
        failed = 'failed'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer(), db.ForeignKey(Task.id))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    file = db.Column(SolutionFile.as_mutable(su.JSONType))
    commit_sha = db.Column(db.String(50), nullable=True)
    status = db.Column(su.ChoiceType(Status, db.String(10)), default=Status.new, nullable=False)
    logs = db.Column(SolutionLogsFile.as_mutable(su.JSONType), nullable=True)
    mark = db.Column(db.Integer(), default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    update_token = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    branch_name = db.Column(db.String(50))

    task: Task = so.relationship(Task, backref=so.backref("solutions", cascade="all,delete-orphan"))
    user: User = so.relationship(User, backref=so.backref("solutions", cascade="all,delete-orphan"))

    def set_branch_name(self):
        self.branch_name = f"solution-{self.task.code}-{self.user.login}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}"

    def get_update_url(self):
        return urljoin(settings.BASE_URL, url_for('courses.solution_update', update_token=self.update_token))
