import click

from app.models import db
from app.app import app
from app.helper import init_database


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    pass


@cli.command()
def init_db():
    with app.app_context():
        db.create_all()


@cli.command()
def drop_db():
    with app.app_context():
        db.drop_all()


@cli.command()
def demo():
    with app.app_context():
        db.drop_all()
        db.create_all()
        init_database()
