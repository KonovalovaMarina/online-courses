from flask import Blueprint, flash, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from app.auth.decorators import login_required
from app.auth.forms import LoginForm, RegistrationForm
from app.models import db, Course, Enrollment, User
from app.models.user import UserRole

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login/", methods=["post", "get"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.login == form.username.data).first()

        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for("auth.account"))

        flash("Некорректный логин или пароль", "error_login")
        return redirect(url_for("auth.login"))

    return render_template("login.html", form=form, title="Login", page='login')


@auth_bp.route("/register/", methods=["post", "get"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.login == form.username.data).first()

        if not user:
            user = User(login=form.username.data, password=form.password.data, role=UserRole.student)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.account"))
        else:
            flash("На этот логин уже был зарегестрирован аккаунт", "error_register")

    return render_template("register.html", title="Register", form=form, page='register')


@auth_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "message_logout")
    return redirect(url_for("auth.login"))


@auth_bp.route("/account/", methods=['get'])
@login_required
def account():

    if current_user.is_admin():
        return redirect(url_for("auth.admin"))

    course = db.session.query(Course) \
        .join(Enrollment) \
        .filter(Enrollment.user == current_user) \
        .first()

    return render_template("account.html", course=course, title="Account", page='account')


@auth_bp.route("/admin/", methods=["get"])
@login_required(roles=[UserRole.admin])
def admin():
    return render_template("admin.html", title="Admin", page='account')
