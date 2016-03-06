# -*- coding: utf-8 -*-

import os


ERRORS_LIMIT = 1
CHECK_TIME = 5

HOSTS = [(host, 'http') for host in os.environ.get('HOSTS').split(',')]
TELEGRAM_GROUP_ID = os.environ.get('TELEGRAM_GROUP_ID')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
PUSHBULLET_TOKEN = os.environ.get('PUSHBULLET_TOKEN')
EMAILS = [email for email in os.environ.get('EMAILS').split(',')]

MAILDOCKER_API_SECRET = os.environ.get('MAILDOCKER_API_SECRET')
MAILDOCKER_API_KEY = os.environ.get('MAILDOCKER_API_KEY')
MAILDOCKER_DOMAIN = os.environ.get('MAILDOCKER_DOMAIN')
MAILDOCKER_FROM_NAME = os.environ.get('MAILDOCKER_FROM_NAME')
MAILDOCKER_FROM_EMAIL = os.environ.get('MAILDOCKER_FROM_EMAIL')
