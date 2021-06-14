import typing as t
from datetime import datetime, timedelta
from itertools import groupby
from operator import attrgetter

from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for, g
from flask_login import current_user

from app.git_api import commit_solution
from app.auth.decorators import login_required
from app.courses.forms import (
    AddLectureForm, ChangeMarkForm, SelectCourseForm, UpdateSolutionForm, CreateCourseForm,
    SendSolutionForm
)
from app.helper import add_course
from app.models import (
    SolutionLogsFile, TaskSolution, db, Course, Enrollment, Lecture, Task, User, UserRole, SolutionFile,
    StoreManager
)
import sqlalchemy as sa

courses_bp = Blueprint('courses', __name__)


@courses_bp.route("/courses/change_mark/", methods=["post", "get"])
@login_required(roles=[UserRole.admin])
def change_marks():
    g.course_form = course_form = SelectCourseForm()

    form = ChangeMarkForm()

    if course_form.validate_on_submit() and form.validate_on_submit():
        task_solution = db.session.query(TaskSolution).filter_by(
            task=form.task.data, user=form.user.data
        ).order_by(TaskSolution.created_at.desc()).first()

        if task_solution:
            task_solution.mark = form.mark.data
            db.session.commit()

        flash("Оценка была изменена", "success_ch_m")
        return redirect(url_for("courses.change_marks"))

    users = {}
    tasks = {}

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

        users[course.id] = [(u.id, u.login) for u in users_query]
        tasks[course.id] = [(t.id, t.name) for t in tasks_query]

    return render_template(
        "change_mark.html",
        form=form,
        course_form=course_form,
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


@courses_bp.route("/courses/<name>/subscribe", methods=["POST"])
@login_required
def subscribe_course(name):
    course = _get_object_or_404(Course, name=name)
    enrollments_query = db.session.query(Enrollment).filter(Enrollment.user == current_user)
    if db.session.query(enrollments_query.filter(Enrollment.course == course).exists()).scalar():
        flash("Вы уже подписаны на этот курс", "error_courses")
    elif db.session.query(enrollments_query.exists()).scalar():
        flash("Можно записаться только на один курс в семестре", "error_courses")
    else:
        enrollment = Enrollment(user_id=current_user.id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()

    return redirect(request.args.get('next', url_for('courses.list_courses')))


@courses_bp.route("/courses/<name>/unsubscribe", methods=["POST"])
@login_required
def unsubscribe_course(name):
    course = _get_object_or_404(Course, name=name)
    enrollment = db.session.query(Enrollment).filter(
        Enrollment.course == course,
        Enrollment.user == current_user
    ).one_or_none()

    if not enrollment:
        flash("Вы уже отписаны от этого курса", "error_courses")
    else:
        db.session.delete(enrollment)
        db.session.commit()

    return redirect(request.args.get('next', url_for('courses.list_courses')))


@courses_bp.route("/courses/", methods=["GET"])
@login_required
def list_courses():
    courses = db.session.query(Course).all()

    subscriptions = {
        en.course_id for en in
              db.session.query(Enrollment.course_id).filter(Enrollment.user == current_user).all()
    }

    return render_template("courses.html", courses=courses, subscriptions=subscriptions, title="Courses", page='courses')


def _get_object_or_404(model: t.Type[db.Model], **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance is None:
        return abort(status=404, description="Объект не найден")
    return instance


@courses_bp.route("/courses/<name>")
@login_required
def course_details(name):
    course = _get_object_or_404(Course, name=name, is_started=True)
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


def get_solutions(course: Course, user: User = None):
    s = db.session.query(
        TaskSolution,
        sa.func.first_value(TaskSolution.id).over(
            partition_by=TaskSolution.task_id,
            order_by=TaskSolution.created_at.desc()
        ).label("latest_id")
    ).join(Task).join(Lecture).join(User).filter(
        Lecture.course == course
    ).order_by(TaskSolution.user_id, Lecture.id)

    if user is not None:
        s = s.filter(TaskSolution.user == user)
    s = s.subquery('s')
    solutions = db.session.query(TaskSolution).select_entity_from(s).filter(s.c.id == s.c.latest_id)
    return solutions


@courses_bp.route("/courses/<name>/marks")
@login_required
def marks(name: str):
    course = _get_object_or_404(Course, name=name)
    solutions = get_solutions(course, current_user)
    return render_template("marks.html", title="Marks", solutions=solutions, course=course, page='marks')


@courses_bp.route("/marks_table/", methods=["post", "get"])
@login_required(roles=[UserRole.admin])
def marks_table():

    def _get_mark_table():
        for course in db.session.query(Course).all():
            tasks = db.session.query(Task).join(Lecture).filter(Lecture.course == course).order_by(Task.id).all()
            tasks_index = {t.id: i for i, t in enumerate(tasks)}
            users = set(db.session.query(User).join(Enrollment).filter(Enrollment.course==course).all())

            def _get_user_solutions():
                solutions = get_solutions(course=course)
                for user, user_solutions in groupby(solutions, key=attrgetter('user')):
                    _user_solutions = [None] * len(tasks)
                    for s in user_solutions:
                        _user_solutions[tasks_index[s.task_id]] = s
                    users.discard(user)
                    yield user, _user_solutions
                for user in users:
                    yield user, [None] * len(tasks)

            yield course, tasks, _get_user_solutions()

    return render_template(
        "marks_table.html",
        title="Marks_table",
        users_marks=_get_mark_table(),
        page='marks_table'
    )
