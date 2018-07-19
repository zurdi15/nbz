#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import sys
import time
import datetime


class Logging:
    """Logger library to show the output of the script

    This library provides a way to log each step of an nbz-script, showing if it is going right,
    or if an error occurs.
    """

    def __init__(self):
        """Inits Logging class"""

        pass


    @staticmethod
    def log(level, msg):
        """Print the log in terminal

        Args:
            level: this parameter indicates if the message to print is a log message or an error message
            msg: message to print in terminal
        """

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
            print("{GREEN}  -  NBZ Log{YELLOW}[{st}]: {NC}{msg}".format(GREEN=GREEN, 
                                                                        YELLOW=YELLOW, 
                                                                        NC=NC, 
                                                                        st=st, 
                                                                        msg=msg))
        elif level == 'ERROR':
            print("{RED}  -  NBZ Log{YELLOW}[{st}]: {NC}{msg}".format(RED=RED, 
                                                                      YELLOW=YELLOW, 
                                                                      NC=NC, 
                                                                      st=st, 
                                                                      msg=msg))
        else:
            print('Not defined logger level: {level}'.format(level=level))

