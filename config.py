CSRF_ENABLED = True
SECRET_KEY = 'ThisPassWordDefinitelyNeedsToBeChanged'
import os
basedir = os.path.abspath(os.path.dirname(__file__))
MONGODB_SETTINGS = {
    'DB': 'pycommappdb'
}