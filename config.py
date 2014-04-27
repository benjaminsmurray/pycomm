CSRF_ENABLED = True
SECRET_KEY = 'ThisPassWordDefinitelyNeedsToBeChanged'
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pycommappdb.db')