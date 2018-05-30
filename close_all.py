#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

import sys
import os
import psutil
import signal

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'lib'))

from lib_log_nbz import Logging
logger = Logging()

this_process_pid = psutil.Process(os.getpid()).ppid()
os.kill(this_process_pid, signal.SIGTERM)
#os.killpg(this_process_pid, 9)
logs = ['geckodriver.log', 'bmp.log', 'server.log']
for log in logs:
    if os.path.isfile(os.path.join(os.getcwd(), log)):
        os.remove(os.path.join(os.getcwd(), log))
