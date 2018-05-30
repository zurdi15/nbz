#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

import sys
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'lib'))

from lib_log_nbz import Logging
logger = Logging()


this_process_pid = os.getppid()
logs = ['bmp.log', 'geckodriver.log', 'server.log']
for log in logs:
        if os.path.isfile(os.path.join(os.getcwd(), log)):
                os.remove(os.path.join(os.getcwd(), log))
logger.log('NOTE', 'Connections closed')
os.killpg(this_process_pid, 9)
