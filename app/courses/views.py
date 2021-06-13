import typing as t
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user

from app.git_api import commit_solution
from app.auth.decorators import login_required
from app.courses.forms import AddLectureForm, ChangeMarkForm, UpdateSolutionForm, CreateCourseForm, SendSolutionForm
from app.helper import COURSES, add_course
from app.models import (
    SolutionLogsFile, TaskSolution, db, Course, Enrollment, Lecture, Mark, Module, Task, User, UserRole, SolutionFile,
    StoreManager
)

courses_bp = Blueprint('courses', __name__)


@courses_bp.route("/courses/change_mark/", methods=["post", "get"])
@login_required(roles=[UserRole.admin])
def change_marks():
    form = ChangeMarkForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.login == form.username.data).first()
        task = db.session.query(Task).filter(Task.name == form.task_name.data).first()
        task_solution = db.session.query(TaskSolution).filter_by(
            task=task, user=user
        ).order_by(TaskSolution.created_at.desc()).first()

        if task_solution:
            task_solution.mark = form.mark.data
            db.session.commit()

        flash("Оценка была изменена", "success_ch_m")
        return redirect(url_for("courses.change_marks"))

    users: t.Dict[str, t.List[str]] = defaultdict(list)
    tasks: t.Dict[str, t.List[str]] = defaultdict(list)

    for course in db.session.query(Course).all():
        users_query = db.session.query(User) \
            .join(Enrollment) \
            .join(Course, Enrollment.course_id == Course.id) \
            .filter(Course.id == course.id) \
            .all()

        tasks_query = db.session.query(Task) \
            .join(Lecture, Task.lecture_id == Lecture.id) \
            .join(Course, Lecture.course_id == Course.id) \
            .filter(Course.id == course.id) \
            .all()

        for user in users_query:
            users[course.name].append(user.login)

        for task in tasks_query:
            tasks[course.name].append(task.name)
    return render_template(
        "change_mark.html",
        form=form,
        tasks=tasks,
        users=users,
        title="Change mark",
        page='change mark'
    )


@courses_bp.route("/courses/start/", methods=["post", "get"])
@login_required(roles=[UserRole.admin])
def start_course():
    courses = db.session.query(Course).filter_by(is_started=False).all()
    for course in courses:
        if course.name + '_start' in request.form:

            if course:
                course.is_started = True
                db.session.flush()

            start = datetime.now()

            for i, lecture in enumerate(course.lectures, 1):
                for task in lecture.tasks:
                    task.deadline = start + timedelta(days=i * 7)

            db.session.commit()
            flash("Запущен курс " + course.name, "success_start_course")

            return redirect(url_for("courses.start_course"))

    return render_template("start_course.html", courses=courses, title="Start course", page='start course')


@courses_bp.route("/courses/create/", methods=["post", "get"])
@login_required(roles=[UserRole.admin])
def create_course():
    courses = db.session.query(Course).all()
    print([c.name for c in courses])

    form_course = CreateCourseForm()
    if form_course.validate_on_submit():
        add_course(form_course.course_name)

    form_lecture = AddLectureForm()
    if form_lecture.validate_on_submit():
        print(form_lecture.lecture_name)
        # add_modules(db, name_course, list_modules)
        # add_lectures(db, list_lectures)

    return render_template(
        "create_course.html",
        form_course=form_course,
        form_lecture=form_lecture,
        courses=[c.name for c in courses],
        title="Create course",
        page='create course'
    )


@courses_bp.route("/courses/", methods=["post", "get"])
@login_required
def list_courses():
    courses = db.session.query(Course).all()

    for course in courses:
        if course.name + '_subscribe' in request.form:

            if not db.session.query(Enrollment).filter(Enrollment.user_id == current_user.id).first():
                enrollment = Enrollment(user_id=current_user.id, course_id=course.id)
                db.session.add(enrollment)
                db.session.commit()
            else:
                flash("Можно записаться только на один курс в семестре", "error_courses")

        if course.name + '_unsubscribe' in request.form:
            enrollment = db.session.query(Enrollment).filter(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == course.id
            ).first()

            if enrollment:
                db.session.delete(enrollment)
                db.session.commit()

    enroll = [en[0] for en in
              db.session.query(Enrollment.course_id).filter(Enrollment.user_id == current_user.id).all()]

    return render_template("courses.html", courses=courses, enroll=enroll, title="Courses", page='courses')


def _get_object_or_404(model: t.Type[db.Model], **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance is None:
        return abort(status=404, description="Объект не найден")
    return instance


@courses_bp.route("/courses/<name>")
@login_required
def course_details(name):
    course = _get_object_or_404(Course, name=name)
    lectures = db.session.query(Lecture).filter(
        Lecture.course_id == course.id
    ).all()
    return render_template("course.html", course_name=name, lectures=lectures)


@courses_bp.route("/courses/<course_name>/<lecture_name>")
@login_required
def lecture_details(course_name, lecture_name):
    course = _get_object_or_404(Course, name=course_name, is_started=True)
    lecture = _get_object_or_404(Lecture, course_id=course.id, name=lecture_name)
    tasks = db.session.query(Task).filter_by(lecture_id=lecture.id)
    return render_template("lecture.html", course=course_name, lecture=lecture, tasks=tasks)


@courses_bp.route("/tasks/<task_id>", methods=['GET', 'POST'])
@login_required
def task_details(task_id):
    task = _get_object_or_404(Task, id=task_id)

    if not task.lecture.course.is_started:
        return abort(status=404, description="Объект не найден")

    solutions = db.session.query(TaskSolution).filter_by(task=task, user=current_user).order_by(
        TaskSolution.created_at).all()

    with StoreManager(db.session):
        form = SendSolutionForm()
        if form.validate_on_submit():
            solution = TaskSolution(
                task=task,
                user=current_user,
                file=SolutionFile.create_from(form.file.data, extension='.py')
            )
            solution.set_branch_name()
            db.session.add(solution)
            db.session.flush()
            solution.commit_sha = commit_solution(solution)
            db.session.commit()

            return redirect(url_for('courses.task_details', task_id=task.id))

        return render_template(
            "task_details.html",
            course=task.lecture.course,
            lecture=task.lecture,
            task=task,
            form=form,
            solutions=solutions,
        )


@courses_bp.route("/solutions/<update_token>/update", methods=["POST"])
def solution_update(update_token):
    solution: TaskSolution = _get_object_or_404(TaskSolution, update_token=update_token)

    with StoreManager(db.session):
        form = UpdateSolutionForm()
        if form.validate_on_submit():
            if form.logs.data:
                solution.logs = SolutionLogsFile.create_from(form.logs.data, extension='.log')

            solution.status = TaskSolution.Status(form.status.data)

            if solution.status == TaskSolution.Status.done:

                if datetime.now() <= solution.task.deadline:
                    solution.mark = 10
                else:
                    solution.mark = 5

            db.session.commit()
        else:
            response = make_response(str(form.errors), 400)
            response.mimetype = "text/plain"
            return response

    response = make_response("OK", 200)
    response.mimetype = "text/plain"
    return response


@courses_bp.route("/courses/<int:course_id>/marks")
@login_required
def marks(course_id: int):
    course = _get_object_or_404(Course, id=course_id)
    solutions = db.session.query(TaskSolution).join(Task).join(Lecture).join(User).filter(
        Lecture.course_id == course_id,
        Task.user == current_user
    )
    return render_template("marks.html", title="Marks", user_marks=user_marks, course=course, page='marks')


@courses_bp.route("/marks_table/", methods=["post", "get"])
@login_required(roles=[UserRole.admin])
def marks_table():
    users_marks: t.Dict[str, t.Dict[str, t.List[t.Tuple[str, str]]]] = {}

    for course_name in COURSES:
        users_marks[course_name] = {}
        course = db.session.query(Course).filter(Course.name == course_name).first()
        names_query = (db.session.query(Course, Enrollment, User)
                       .join(Course, Enrollment.course_id == Course.id)
                       .join(User, User.id == Enrollment.user_id)
                       .filter(Course.name == course_name)
                       .all())

        for _, _, user in names_query:
            users_marks[course_name][user.login] = []
            user_marks = (
                db.session.query(User, Mark, Module)
                    .join(Mark, User.id == Mark.user_id)
                    .join(Module, Module.id == Mark.module_id)
                    .filter(User.login == user.login)
                    .filter(Module.course_id == course.id)
                    .all()
            )

            for _, mark, module in user_marks:
                users_marks[course_name][user.login].append((module.name, mark.mark))

    return render_template(
        "marks_table.html",
        title="Marks_table",
        users_marks=users_marks,
        page='marks_table'
    )
