# -*- coding: utf-8 -*-

import socket, sys
from datetime import datetime
from urllib.parse import urlparse

smtp_response = '220'
http_ok_response = 'HTTP/1.1 200 OK'
http_not_found_response = 'HTTP/1.1 404 Not Found'
http_redirect_response = 'HTTP/1.1 301 Moved Permanently'

http_dialog = """
GET {} HTTP/1.1
HOST: {}

"""


def connect(host, port, dialog=b''):

    try:
        s = None
        for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, _, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except OSError as msg:
                s = None
                continue
            try:
                s.connect(sa)
            except OSError as msg:
                s.close()
                s = None
                continue
            break

        if s is None:
            print('could not open socket')
            sys.exit(1)

        s.sendall(dialog)
        data = s.recv(1024).decode("utf-8")
        s.close()

    except Exception as e:
        print("something's wrong with %s:%d. Exception is %s" % e)
    finally:
        s.close()
    print(data)
    return data.split('\r\n')[0]


def check_smtp(host):
    port = 25
    start_time = datetime.now()
    result = connect(host, port).split(' ')[0] == smtp_response
    response_time = int((datetime.now() - start_time).total_seconds() * 1000)
    return result, response_time


def check_http(host):
    if 'https' in host:
        port = 443
    else:
        port = 80
    parse_object = urlparse(host)
    host = parse_object.netloc
    path = parse_object.path
    dialog = bytes(http_dialog.format(path, host), 'utf-8')
    start_time = datetime.now()
    result = connect(host, port, dialog) == http_ok_response
    response_time = int((datetime.now() - start_time).total_seconds() * 1000)
    return result, response_time
