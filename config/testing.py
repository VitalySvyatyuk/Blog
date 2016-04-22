import os

DEBUG = False
TESTING = True
SECRET_KEY = 'secretico'
WTF_CSRF_ENABLED = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../test_data.sqlite3')