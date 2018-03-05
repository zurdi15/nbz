#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

class Logging:

    def __init__(self):
        pass

    @staticmethod
    def log(level, msg):
        if level == 'NOTE':
            print('NB - Log' + ': ' + msg)
        elif level == 'ERROR':
            print('NB - Error' + ': ' + msg)
        else:
            print('Not defined logger level: ' + str(level))
