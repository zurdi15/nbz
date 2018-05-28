#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import time
import datetime


class Logging:

    def __init__(self):
        pass

    @staticmethod
    def log(level, msg):
        
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        if level == 'NOTE':
            print("\033[92m  -  NBZ Log\033[93m[{st}]: \033[0m{msg}".format(st=st, msg=msg))
            #print("\033[92m" + '  - NBZ Log\033[93m[' + st + ']: ' + "\033[0m" + msg)
        elif level == 'ERROR':
            print("\033[91m  -  NBZ Log\033[93m[{st}]: \033[0m{msg}".format(st=st, msg=msg))
            #print("\033[91m" + '  - NBZ Error\033[93m[' + st + ']: ' + "\033[0m" + msg)
        else:
            print('Not defined logger level: {level}'.format(level=level))
