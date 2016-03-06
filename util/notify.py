# -*- coding: utf-8 -*-

import json
import requests
import telepot

from settings import TELEGRAM_TOKEN, PUSHBULLET_TOKEN, EMAILS, TELEGRAM_GROUP_ID

PUSHBULLET_URL = 'https://api.pushbullet.com/v2/pushes'
PUSHBULLET_HEADERS = {'content-type': 'application/json'}
PUSHBULLET_PAYLOAD = {'type': 'note'}

bot = telepot.Bot(TELEGRAM_TOKEN)

class Notify(object):

    def __init__(self):
        self.message = {}
        self.pushbullet_token = PUSHBULLET_TOKEN

    def using_pushbullet(self):
        self.send_note_to_pushbullet()

    def using_email(self):
        for email in EMAILS:
            self.email = email
            self.send_email()

    def using_telegram(self):
        self.send_message_to_telegram()

    def notify(self):
        self.using_pushbullet()
        self.using_telegram()
        self.using_email()

    def problem(self, host, check_type):
        self.message['title'] = '[CRITICAL] - {} está com problemas'.format(host)
        self.message['body'] = 'Não consegui acessar o serviço {} em {}'.format(check_type, host)
        self.notify()

    def recovery(self, host, check_type, error_time):
        self.message['title'] = (
            '[RECOVERY] - Serviço {} restaurado no servior {}'.format(check_type, host)
        )
        self.message['body'] = (
            'Serviço {} restaurado no servior {} após {}s'.format(check_type, host, error_time)
        )
        self.notify()

    def send_message_to_telegram(self):
        bot.sendMessage(TELEGRAM_GROUP_ID, self.message['body'])

    def send_note_to_pushbullet(self):
        PUSHBULLET_HEADERS['Access-Token'] = self.pushbullet_token
        PUSHBULLET_PAYLOAD['title'] = self.message['title']
        PUSHBULLET_PAYLOAD['body'] = self.message['body']
        requests.post(
            PUSHBULLET_URL,
            data=json.dumps(PUSHBULLET_PAYLOAD),
            headers=PUSHBULLET_HEADERS
        )

    def send_email(self):
        PUSHBULLET_HEADERS['Access-Token'] = self.pushbullet_token
        PUSHBULLET_PAYLOAD['title'] = self.message['title']
        PUSHBULLET_PAYLOAD['body'] = self.message['body']
        PUSHBULLET_PAYLOAD['email'] = self.email
        requests.post(
            PUSHBULLET_URL,
            data=json.dumps(PUSHBULLET_PAYLOAD),
            headers=PUSHBULLET_HEADERS
        )

