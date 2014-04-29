from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.httpauth import HTTPBasicAuth
import os
from config import basedir

#create flask object and other flask objects. global
flaskApp = Flask(__name__)
flaskApp.config.from_object('config')

flaskdb  = MongoEngine()
flaskdb.init_app(flaskApp)
flaskAuth = HTTPBasicAuth()
flaskMigrate = Migrate(flaskApp, flaskdb)
flaskManager = Manager(flaskApp)
flaskManager.add_command('flaskdb', MigrateCommand)

from app import models, views