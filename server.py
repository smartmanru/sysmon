# -*- coding: utf-8 -*-

from time import sleep, time

from daemonize import Daemonize

from settings import DEBUG, HOSTS, ERRORS_LIMIT, CHECK_TIME
from util.check_types import check_http, check_smtp
from util.notify import Notify


def main():

    errors = {}
    start_time = {}
    notify = Notify()

    for host, check_type in HOSTS:
        errors[host + '_' + check_type] = 0
        start_time[host + '_' + check_type] = None

    while True:
        for host in HOSTS:
            host, check_type = host

            if check_type == 'http':
                result, response_time = check_http(host)

            elif check_type == 'smtp':
                result, response_time = check_smtp(host)

            if not result or DEBUG:
                errors[host + '_' + check_type] += 1
                if not start_time[host + '_' + check_type]:
                    start_time[host + '_' + check_type] = time()
                if errors[host + '_' + check_type] == ERRORS_LIMIT:
                    notify.problem(host, check_type)
            else:
                if errors[host + '_' + check_type] >= ERRORS_LIMIT:
                    error_time = round(time() - start_time[host + '_' + check_type])
                    notify.recovery(host, check_type, error_time)

                errors[host + '_' + check_type] = 0
                start_time[host + '_' + check_type] = None

            if DEBUG:
                print(host, check_type, errors[host + '_' + check_type]), response_time
                print(host, check_type, start_time[host + '_' + check_type])

        sleep(CHECK_TIME)

pid = "/tmp/test.pid"
daemon = Daemonize(app="test_app", pid=pid, action=main, foreground=DEBUG)
daemon.start()
