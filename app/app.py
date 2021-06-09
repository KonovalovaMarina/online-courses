from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from app import settings
from app.auth.views import auth_bp
from app.courses.views import courses_bp
from app.models import User, db
from app.views import main_bp

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "a really really really really long secret key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URI

db.init_app(app)

bootstrap: Bootstrap = Bootstrap(app)
app.register_blueprint(auth_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(main_bp)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
