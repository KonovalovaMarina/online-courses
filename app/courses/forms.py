from flask import g
from flask_wtf import FlaskForm
from wtforms import (
    FieldList, FormField, IntegerField, SelectField, StringField, SubmitField, FileField,
    validators
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, ValidationError, NumberRange

from app.models import Course, Enrollment, Lecture, Task, TaskSolution, User, UserRole, db


class SelectCourseForm(FlaskForm):
    course = QuerySelectField(
        "Курс",
        query_factory=lambda: db.session.query(Course).all(),
        get_label="name",
        allow_blank=True,
        blank_text="-------",
        validators=[InputRequired()]
    )


def course_users_query():
    query = db.session.query(User) \
        .join(Enrollment) \
        .join(Course)

    if g.course_form.course.data is not None:
        query = query.filter(Course.id == g.course_form.course.data.id)
    else:
        query = query.filter(False)
    return query.all()


def course_tasks_query():
    query = db.session.query(Task) \
        .join(Lecture) \
        .join(Course)
    if g.course_form.course.data is not None:
        query = query.filter(Course.id == g.course_form.course.data.id)
    else:
        query = query.filter(False)
    return query.all()


class ChangeMarkForm(FlaskForm):
    user = QuerySelectField(
        "Студент",
        query_factory=course_users_query,
        get_label="login",
        allow_blank=True,
        blank_text="-------",
        validators=[InputRequired()]
    )
    task = QuerySelectField(
        "Практика",
        query_factory=course_tasks_query,
        get_label="name",
        allow_blank=True,
        blank_text="-------",
        validators=[InputRequired()]
    )
    mark = IntegerField("Оценка", validators=[NumberRange(min=0, max=10)])
    submit = SubmitField("ОК")


class CreateCourseForm(FlaskForm):
    course_name = StringField("Название курса", validators=[InputRequired()])
    submit = SubmitField("ОК")


class AddLectureForm(FlaskForm):
    course_name_lecture = SelectField("Курс")
    lecture_name = StringField("Название лекции", validators=[InputRequired()])
    lecture_video = StringField("Ссылка на видео", validators=[InputRequired()])
    submit = SubmitField("ОК")


class AddLectures1Form(FlaskForm):
    lectures = FieldList(FormField(AddLectureForm))
    submit = SubmitField("ОК")


class AddLecturesForm(FlaskForm):
    lectures = FieldList(StringField("Лекция"))
    submit = SubmitField("ОК")


class SendSolutionForm(FlaskForm):
    file = FileField(validators=[validators.required()])

    def validate_file(self, field):
        if field.data and not field.data.filename.endswith('.py'):
            raise ValidationError('Некорректный формат файла')


class UpdateSolutionForm(FlaskForm):
    logs = FileField()
    status = SelectField(choices=[
        (TaskSolution.Status.done.value, TaskSolution.Status.done.value),
        (TaskSolution.Status.failed.value, TaskSolution.Status.failed.value),
        (TaskSolution.Status.testing.value, TaskSolution.Status.testing.value),
    ], validators=[validators.required()])

    class Meta(FlaskForm.Meta):
        csrf = False
