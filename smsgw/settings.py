# -*- coding: utf-8 -*-
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

import os
import multiprocessing
from kombu import Queue
from smsgw.lib.utils import get_sql_alchemy_db_uri, get_rabbitmq_uri


SERVER_NAME = os.environ.get('NGINX_HOSTNAME')

DEBUG = os.environ.get('DEBUG', False)
TESTING = os.environ.get('TESTING', False)
STATIC_FOLDER = os.path.join('static')
SECRET_KEY = os.urandom(24)

# Logging
LOGGING = bool(os.environ.get('LOGGING', False))
LOGGING_EMAIL_BLACKLIST = {
    # TODO(vojta) figure out what endpoints should be blacklisted
}

# Database
DATABASE_DIALECT = 'mysql'
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'db')
DATABASE_PORT = os.environ.get('DATABASE_PORT', 3306)
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
SQLALCHEMY_DATABASE_URI = get_sql_alchemy_db_uri(
    dialect=DATABASE_DIALECT,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME
)
# http://stackoverflow.com/questions/18054224/python-sqlalchemy-mysql-server-has-gone-away
SQLALCHEMY_POOL_RECYCLE = 60

# RabbitMQ
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST', 'smsgw')
RABBITMQ_USER = os.environ.get('RABBITMQ_DEFAULT_USER', 'guest')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')

# Mail
MAIL_DEFAULT = os.environ.get('MAIL_DEFAULT', 'hi@vojtech.me')
MAIL_DEBUG = os.environ.get('MAIL_DEBUG', 'hi@vojtech.me')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

# CELERY
CELERY_IMPORTS = ("smsgw.tasks.callback", "smsgw.tasks.mail")
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = get_rabbitmq_uri(
    host=RABBITMQ_HOST,
    vhost=RABBITMQ_VHOST,
    user=RABBITMQ_USER,
    password=RABBITMQ_PASSWORD
)
CELERY_RESULT_BACKEND = None
CELERY_IGNORE_RESULT = True
CELERY_QUEUES = (Queue('callbacks', routing_key='callbacks'),
                 Queue('mails', routing_key='mails'))
CELERYBEAT_SCHEDULE = None
CELERYD_POOL_RESTARTS = True
CELERY_ALWAYS_EAGER = TESTING
CELERY_EAGER_PROPAGATES_EXCEPTIONS = TESTING
CELERY_ACCEPT_CONTENT = ['pickle']

# Gammu
GAMMU_VERSION = os.environ.get('GAMMU_VERSION', "1.34.0")
GAMMU_DATABASE_VERSION = os.environ.get('GAMMU_DATABASE_VERSION', 14)
GAMMU_DEVICE_SERIAL = os.environ.get('GAMMU_DEVICE_SERIAL', '/dev/ttyUSB0')
GAMMU_DEVICE_CONNECTION = os.environ.get('GAMMU_DEVICE_CONNECTION', 'at')
GAMMU_DEVICE_ID = os.environ.get('GAMMU_DEVICE_ID', 'tmobile-huawei')
GAMMU_DEVICE_PIN = os.environ.get('GAMMU_DEVICE_PIN')
