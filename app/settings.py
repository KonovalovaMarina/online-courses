import os

DB_URI: str = os.environ.get('DB_URI', "postgresql+psycopg2://academy:12345678@localhost:5436/academy")
SOLUTIONS_REPO_URI = os.environ.get('SOLUTIONS_REPO_URI', 'git@gitlab.com:konovalova.owl/online-courses-admin.git')
SOLUTIONS_REPO_PATH = os.environ.get('SOLUTIONS_REPO_PATH', 'solutions_repo')
SOLUTIONS_REPO_SSH_KEY = os.environ.get('SOLUTIONS_REPO_SSH_KEY', '/Users/macbook/.ssh/id_rsa_marina')

BASE_URL = os.environ.get('BASE_URL', "https://online-courses.eu.ngrok.io")
