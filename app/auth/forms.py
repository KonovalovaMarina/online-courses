from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired()])
    password = PasswordField("Пароль", validators=[InputRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("ОК")


class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired()])
    password = PasswordField(
        "Пароль",
        validators=[InputRequired(), EqualTo("confirm", message="Пароли не совпадают")],
    )
    confirm = PasswordField("Повторите пароль", validators=[InputRequired()])
    submit = SubmitField("ОК")
