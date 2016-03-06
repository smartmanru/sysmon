# -*- coding: utf-8 -*-

from time import sleep, time
import signal

from daemonize import Daemonize
import gevent

from settings import DEBUG, FOREGROUND, HOSTS, ERRORS_LIMIT, CHECK_TIME
from util.check_types import check_http, check_smtp
from util.notify import Notify


def check(host):
    notify = Notify()
    host, check_type = host
    errors = 0
    start_time = None

    while True:

        if check_type == 'http':
            result, response_time = check_http(host)

        elif check_type == 'smtp':
            result, response_time = check_smtp(host)

        if not result:
            errors += 1
            if not start_time:
                start_time = time()
            if errors == ERRORS_LIMIT:
                notify.problem(host, check_type)
        else:
            if errors >= ERRORS_LIMIT:
                error_time = round(time() - start_time)
                notify.recovery(host, check_type, error_time)

            errors = 0
            start_time = None

        if DEBUG:
            print(host, check_type, errors, response_time)

        gevent.sleep(CHECK_TIME)


def main():
    gevent.signal(signal.SIGQUIT, gevent.kill)
    gevent.joinall([gevent.spawn(check, host) for host in HOSTS])

pid = "/tmp/test.pid"
daemon = Daemonize(app="test_app", pid=pid, action=main, foreground=FOREGROUND)
daemon.start()
