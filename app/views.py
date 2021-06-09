from flask import Blueprint, render_template, send_from_directory

from app.forms import Sample


main_bp = Blueprint('main', __name__)


@main_bp.route('/media/<path:name>')
def send_media(name):
    return send_from_directory(f'uploads', name, as_attachment=True)


@main_bp.route("/", methods=['post', 'get'])
def home():
    return render_template("index.html", title="Home", page='home')


@main_bp.route('/test', methods=['GET', 'POST'])
def sample_form():
    form = Sample()
    if form.validate_on_submit():
        if form.flist.data:
            for item in form.flist.data:
                print(item)
    return render_template('test.html', form=form)
