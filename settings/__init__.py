# -*- coding: utf-8 -*-

import os


ERRORS_LIMIT = 100
CHECK_TIME = 5

HOSTS = [(host, 'http') for host in os.environ.get('HOSTS').split(',')]
TELEGRAM_GROUP_ID = os.environ.get('TELEGRAM_GROUP_ID')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
PUSHBULLET_TOKEN = os.environ.get('PUSHBULLET_TOKEN')
EMAILS = [email for email in os.environ.get('EMAILS').split(',')]
