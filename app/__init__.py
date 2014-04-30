from flask import Flask
from mongoengine import connect
from flask.ext.script import Manager
from flask.ext.httpauth import HTTPBasicAuth
import os
import config


#create flask object and other flask objects
flaskApp = Flask("pycomm")
flaskApp.config.from_object('config')

connect(config.MONGODB_SETTINGS)
auth = HTTPBasicAuth()
flaskManager = Manager(flaskApp)

from app import models, views