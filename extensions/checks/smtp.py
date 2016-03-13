# -*- coding: utf-8 -*-

from datetime import datetime

smtp_response = '220'


class SmtpCheck(BaseCheck):

    def check(self):
        port = 25
        start_time = datetime.now()
        result = self.connect(self.host, port).split(' ')[0] == smtp_response
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        return result, response_time


