# -*- coding: utf-8 -*-

from datetime import datetime
from urlparse import urlparse

from extensions.checks.base import BaseCheck

http_dialog = """
GET {} HTTP/1.1
HOST: {}

"""

http_ok_response = 'HTTP/1.1 200 OK'
http_not_found_response = 'HTTP/1.1 404 Not Found'
http_redirect_response = 'HTTP/1.1 301 Moved Permanently'


class HttpCheck(BaseCheck):
    def check(self):
        if 'https' in self.host:
            # TODO: use requests to check
            return False, 0
        else:
            port = 80
        parse_object = urlparse(self.host)
        host = parse_object.netloc
        path = parse_object.path
        dialog = bytes(http_dialog.format(path, host).encode('utf-8'))
        start_time = datetime.now()
        result = self.connect(host, port, dialog) == http_ok_response
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        return result, response_time
