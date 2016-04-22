import os

DEBUG = True
SECRET_KEY = 'secretico'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../dev_data.sqlite3')