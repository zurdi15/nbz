#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import sys
import time
import datetime


class Logging:

    def __init__(self):
        pass

    @staticmethod
    def log(level, msg):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        if os.name == 'posix':
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            RED = '\033[91m'
            NC = '\033[0m'
        else:
            GREEN = ''
            YELLOW = ''
            RED = ''
            NC = ''

        if level == 'NOTE':
            print("{GREEN}  -  NBZ Log{YELLOW}[{st}]: {NC}{msg}".format(GREEN=GREEN, YELLOW=YELLOW, NC=NC, st=st, msg=msg))
        elif level == 'ERROR':
            print("{RED}  -  NBZ Log{YELLOW}[{st}]: {NC}{msg}".format(RED=RED, YELLOW=YELLOW, NC=NC, st=st, msg=msg))
        else:
            print('Not defined logger level: {level}'.format(level=level))
