# coding: utf-8

import importlib
import socket, sys

from gevent import monkey
monkey.patch_all()


from extensions import *


class MetaRegister(type):

    check_options = {}

    def __new__(mcs, name, bases, attrs):
        """ @param name: Name of the class
            @param bases: Base classes (tuple)
            @param attrs: Attributes defined for the class
        """
        new_cls = type.__new__(mcs, name, bases, attrs)
        mcs.check_options[name.replace('Check', '').lower()] = new_cls
        return new_cls


class BaseCheck(object):

    __metaclass__ = MetaRegister

    def __init__(self, host):
        self.host = host

    def connect(self, host, port, dialog=b''):
        data = ''
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
                print 'Could not open socket'
                sys.exit(1)

            s.sendall(dialog)
            data = s.recv(1024).decode("utf-8")
            s.close()

        except Exception as e:
            print 'Something\'s wrong with %s:%d. Exception is %s' % e
        finally:
            s.close()
        return data.split('\r\n')[0]

    def check(self):
        pass


def _load_check_modules():
    available_checks = ['http']
    try:
        for check_name in available_checks:
            importlib.import_module('extensions.checks.{}'.format(check_name))
    except Exception as e:
        raise Exception('load_check_error: {}'.format(e))

_load_check_modules()
