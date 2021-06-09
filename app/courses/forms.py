from flask_wtf import FlaskForm
from wtforms import (
    FieldList, Form, FormField, IntegerField, SelectField, StringField, SubmitField, FileField,
    validators
)
from wtforms.validators import InputRequired, ValidationError

from app.models import TaskSolution


class ChangeMarkForm(FlaskForm):
    course_name = SelectField("Курс")
    username = SelectField("Студент")
    module_name = SelectField("Практика")
    mark = IntegerField("Оценка")
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
