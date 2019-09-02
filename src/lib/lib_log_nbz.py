#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import time
import datetime


class Logging:
	"""Logger library to show the output of the script

	This library provides a way to log each step of an nbz-script, showing if it is going right,
	or if an error occurs.

	Methods:
		log
	"""

	def __init__(self):
		"""Init Logging class"""

		if os.name == 'posix':
			self.GREEN = '\033[92m'
			self.YELLOW = '\033[93m'
			self.RED = '\033[91m'
			self.NC = '\033[0m'
		else:
			self.GREEN = ''
			self.YELLOW = ''
			self.RED = ''
			self.NC = ''

	def log(self, level, msg):
		"""Print the log in terminal

		Args:
			level: this parameter indicates if the message to print is a log message or an error message
			msg: message to print in terminal
		"""

		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		if level == 'NOTE':
			print("{GREEN}  -  NBZ Log{YELLOW}[{st}]: {NC}{msg}".format(GREEN=self.GREEN,
																		YELLOW=self.YELLOW,
																		NC=self.NC,
																		st=st,
																		msg=msg))
		elif level == 'ERROR':
			print("{RED}  -  NBZ Log{YELLOW}[{st}]: {NC}{msg}".format(RED=self.RED,
																	  YELLOW=self.YELLOW,
																	  NC=self.NC,
																	  st=st,
																	  msg=msg))
		else:
			print('Not defined logger level: {level}'.format(level=level))

	def log_header(self):
		print("{YELLOW}  ############################ START NBZ ############################{NC}\n".format(YELLOW=self.YELLOW,
																											NC=self.NC))

	def log_footer(self):
		print("\n{YELLOW}  ############################ END NBZ ############################{NC}\n".format(YELLOW=self.YELLOW,
																											NC=self.NC))

	def log_error(self):
		print("\n{RED}  ************************ ERROR ENDING NBZ ************************{NC}\n".format(RED=self.RED,
																										  NC=self.NC))
