# -*- coding: utf-8 -*-

from time import time
import signal

from daemonize import Daemonize
import gevent

from extensions.checks.base import MetaRegister

from settings import DEBUG, FOREGROUND, HOSTS, ERRORS_LIMIT, CHECK_TIME
from util.notify import Notify


def check(host):
    notify = Notify()
    host, check_type = host
    errors = 0
    start_time = None

    while True:
        service = MetaRegister.check_options[check_type]
        result, response_time = service(host).check()

        if result:
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
daemon = Daemonize(app="sysmon", pid=pid, action=main, foreground=FOREGROUND)
daemon.start()
