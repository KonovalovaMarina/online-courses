from flask import Blueprint, flash, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import redirect

from app.auth.forms import LoginForm, RegistrationForm
from app.helper import init_marks
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
            init_marks(user.id)
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


@auth_bp.route("/account/", methods=['post', 'get'])
@login_required
def account():

    if current_user.is_admin():
        return redirect(url_for("auth.admin"))

    enrolment_with_course = db.session.query(Course, Enrollment) \
        .join(Course, Enrollment.course_id == Course.id) \
        .filter(Enrollment.user_id == current_user.id) \
        .first()

    if enrolment_with_course:
        course, enrollment = enrolment_with_course
        if course.name in request.form:
            db.session.delete(enrollment)
            db.session.commit()
            return render_template("account.html", course="", title="Account", page='account')

        return render_template("account.html", course=course, title="Account", page='account')

    return render_template("account.html", course="", title="Account", page='account')


@auth_bp.route("/admin/", methods=["post", "get"])
@login_required
def admin():
    if current_user.is_admin():
        return render_template("admin.html", title="Admin", page='account')
    else:
        return render_template("account.html", title="Account", page='account')
