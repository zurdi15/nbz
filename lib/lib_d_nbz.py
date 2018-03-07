#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
from lib_log_nbz import *
logger = Logging()


def cast_int(browser, params):
	"""
	Cast numeric string | float value to integer
	"""

	try:
		return int(params[0])
	except Exception as e:
		logger.log('ERROR', 'Error casting ' + str(params[0]) + ' to integer: ' + str(e))
		sys.exit(-1)


def cast_float(browser, params):
	"""
	Cast numeric string | integer value to float
	"""
	
	try:
		return float(params[0])
	except Exception as e:
		logger.log('ERROR', 'Error casting ' + str(params[0]) + ' to float: ' + str(e))
		sys.exit(-1)


def cast_str(browser, params):
	"""
	Cast numeric value to string
	"""
	
	try:
		return str(params[0])
	except Exception as e:
		logger.log('ERROR', 'Error casting ' + str(params[0]) + ' to string: ' + str(e))
		sys.exit(-1)


def sub_str(browser, params):
	"""
	Returns substring from bigger string
	"""

	try:
		if len(params) == 2:
			return params[0][params[1]:]
		else:
			return params[0][params[1]:params[2]]
	except Exception as e:
		logger.log('ERROR', 'Error getting subtring from ' + str(params[0]) + ': ' + str(e))
		sys.exit(-1)


def lenght(browser, params):
	"""
	Returns lenght from any compatible data
	"""
		
	try:
		return len(params[0])
	except Exception as e:
		logger.log('ERROR', 'Error getting lenght from ' + str(params[0]) + ': ' + str(e))
		sys.exit(-1)


def find(browser, params):
	"""
	Search one string into another string
	If it is found, returns starting position of the string searched
	If dont, returns -1
	"""

	try:
		return params[0].find(params[1])
	except Exception as e:
		logger.log('ERROR', 'Error searching substring into ' + str(params[0]) + ': ' + str(e))
		sys.exit(-1)
