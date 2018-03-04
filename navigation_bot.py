#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Alejandro Atance>


import sys
import os
import time
import traceback
import argparse
import pickle
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

sys.path.append(BASE_DIR + 'lib')
sys.path.append(BASE_DIR + 'data')
sys.path.append(BASE_DIR + 'parser')

from lib_logger import Logging
logger = Logging()
from lib_wb_nb import *
from lib_snf_nb import check_net
from parser_nb import NBParser
from features import FEATURES_DICT


class NavigationBot:

	def __init__(self, script, mode, debug=True):

		# Attributes
		self.FEATURES = FEATURES_DICT
		self.USER_FUNC = {}
		
		self.script = script
		self.script_name = os.path.basename(self.script)[0:-4] # Avoiding file extension to use it to name generated files
		self.mode = mode
		self.debug = debug

		self.proxy_path = BASE_DIR + 'proxy/bin/browsermob-proxy'  # Proxy binaries to execute the sniffer
		self.set_browser = False # Flag to instance browser once (even if z_code has more than one instance)
		self.server = None
		self.proxy = None
		self.browser = None

		self.instruction_set = ''
		self.vars_dict = {}

		self.set_net_report = False
		self.net_reports_path = ''
		self.complete_csv_path = ''
		self.complete_csv = None

	    # Execute selected mode
		if self.mode == 'cx':
			self.compile_z_code()
			self.get_z_code()
		elif self.mode == 'c':
			self.compile_z_code()
			logger.log('NOTE', 'Successful compilation of ' + self.script)
			sys.exit(0)
		elif self.mode == 'x':
			self.get_z_code()
		else:
			logger.log('ERROR', 'Not defined compile/execution mode ' + self.mode)
			sys.exit(-1)

		# Do instructions
		self.do_instructions(self.instruction_set)

		# Close browser/proxy/server
		if self.set_browser:
			self.close_all()


	def compile_z_code(self):
		"""
		Compile z_code into object file ready to be executed
		"""
		
		NBParser(self.script)


	def get_z_code(self):
		"""
		Get the compiled z_code object file
		"""
		
		try:
			with open(self.script + 'code') as zcode:
				self.instruction_set = pickle.load(zcode)
			with open(self.script + 'vars') as zcode_vars:
				self.vars_dict = pickle.load(zcode_vars)
			if self.debug:
				logger.log('NOTE', 'Instructions: ' + str(self.instruction_set))
			    logger.log('NOTE', 'Variables: ' + str(self.vars_dict))
		except Exception as e:
			logger.log('ERROR', 'Script not compiled (' + self.script + '): ' + str(e))
			sys.exit(-1)


	def net_report(self, params):
		"""
		Create net report csv
		"""

		self.net_reports_path = BASE_DIR + 'out/net_reports/' + self.script_name
		self.complete_csv_path = self.net_reports_path + '/complete_net_log_' + params[0] + '.csv'
		if not os.path.exists(self.net_reports_path):
			os.makedirs(self.net_reports_path)
		self.complete_csv = open(self.complete_csv_path, 'w')


	def do_instructions(self, instruction_set):
		"""
		Do each instruction from instruction_set (recursively on flow control sentences)
		instruction[0] -> type:
			- assign:		instruction[1] -> id
							instruction[2] -> value | expression

			- def:			instruction[1] -> id
							instruction[2] -> block of sentences

			- func:			instruction[1] -> id
							instruction[2] -> parameters list

			- if:			instruction[1] -> condition
							instruction[2] -> block of sentences (if)
							instruction[3] -> block of sentences (else)

			- for(normal):	instruction[1] -> start index
							instruction[2] -> end index
							instruction[3] -> mode (+ | ++ | - | --)
							instruction[4] -> block of sentences

			- for(foreach): instruction[1] -> iterable variable
							instruction[2] -> list
							instruction[3] -> block of sentences

			- while:		instruction[1] -> condition
							instruction[2] -> block of sentences
		"""

		def get_value(instruction):
			"""
			Local function to get direct value or variable value of a parameter
			Local function to resolve arithmetic expressions
			Local function to resolve boolean expressions
			Local function to resolve funcion return value
			"""

			if isinstance(instruction, list):
				if instruction[0] == 'var':
					return self.vars_dict[instruction[1]]

				elif instruction[0] == 'value':
					return instruction[1]

				elif instruction[0] == 'arithm':
					if instruction[3] == '+':
						op_1 = get_value(instruction[1])
						op_2 = get_value(instruction[2])
						if isinstance(op_1, str) or isinstance(op_2, str):
							return str(op_1) + str(op_2)
						else:
							return op_1 + op_2
					elif instruction[3] == '-':
						return get_value(instruction[1]) - get_value(instruction[2])
					elif instruction[3] == '*':
						return get_value(instruction[1]) * get_value(instruction[2])
					elif instruction[3] == '/':
						return get_value(instruction[1]) / get_value(instruction[2])

				elif instruction[0] == 'boolean':
					if instruction[3] == 'or':
						return get_value(instruction[1]) or get_value(instruction[2])
					elif instruction[3] == 'and':
						return get_value(instruction[1]) and get_value(instruction[2])
					if instruction[3] == '==':
						return get_value(instruction[1]) == get_value(instruction[2])
					if instruction[3] == '<':
						return get_value(instruction[1]) < get_value(instruction[2])
					if instruction[3] == '<=':
						return get_value(instruction[1]) <= get_value(instruction[2])
					if instruction[3] == '>':
						return get_value(instruction[1]) > get_value(instruction[2])
					if instruction[3] == '>=':
						return get_value(instruction[1]) >= get_value(instruction[2])
					if instruction[3] == '!=':
						return get_value(instruction[1]) != get_value(instruction[2])
					if instruction[3] == 'not':
						return not get_value(instruction[1])

				elif instruction[0] == 'func':
					params = []
					for param in instruction[2]:
						params.append(get_value(param))
					if instruction[1] == 'check_net':
						return check_net(self.proxy.har, params)
					else:
						try:
							return self.FEATURES[instruction[1]](self.browser, params)
						except Exception as e:
							logger.log('ERROR', 'Error with function ' + str(e))
							sys.exit(-1)

			else:
				return instruction

		# Main execution loop
		for instruction in instruction_set:
			try:
				if instruction[0] == 'assign':
					self.vars_dict[instruction[1]] = get_value(instruction[2])

				elif instruction[0] == 'def':
					self.USER_FUNC[instruction[1]] = instruction[2]

				elif instruction[0] == 'func':
					params = []
					for param in instruction[2]:
						params.append(get_value(param))
					if instruction[1] == 'browser':
						if not self.set_browser:
							self.server, self.proxy = start_proxy(self.proxy_path)
							self.browser = instance_browser(self.proxy, params)
							self.set_browser = True
						else:
							logger.log('ERROR', 'Browser already instanced')
					elif instruction[1] == 'export_net_report':
							self.net_report(params)
							self.set_net_report = True
					elif instruction[1] == 'check_net':
						pass
					else:
						try:
							if self.FEATURES[instruction[1]]:
								self.FEATURES[instruction[1]](self.browser, params)
							elif self.USER_FUNC[instruction[1]]:
								self.do_instructions(self.USER_FUNC[instruction[1]])
							else:
								logger.log('ERROR', 'Not defined function')
						except Exception as e:
							logger.log('ERROR', 'Error with function ' + str(e))
							sys.exit(-1)

				elif instruction[0] == 'if':
					if get_value(instruction[1]):
						self.do_instructions(instruction[2])
					else:
						if len(instruction) == 4: # If statement have elif OR else
							if instruction[3][0][0] == 'elif':
								for elif_ in instruction[3]:
									if get_value(elif_[1]):
										self.do_instructions(elif_[2])
										break
							elif instruction[3][0][0] == 'else':
								self.do_instructions(instruction[3][0][1])

						elif len(instruction) == 5: # If statement have elif AND else
							elif_done = False
							for elif_ in instruction[3]:
								if get_value(elif_[1]):
									elif_done = True
									self.do_instructions(elif_[2])
									break
							if not elif_done:
								self.do_instructions(instruction[4][0][1])

				elif instruction[0] == 'for':
					if len(instruction) == 4: # Foreach
						element = get_value(instruction[1])
						structure = self.vars_dict[get_value(instruction[2])]
						for aux_element in structure:
							self.vars_dict[element] = aux_element
							self.do_instructions(instruction[3])							
					else: # Standard For
						if instruction[3] == '+':
							for i in xrange(get_value(instruction[1]), get_value(instruction[2]), 1):
								self.do_instructions(instruction[4])
						elif instruction[3] == '++':
							for i in xrange(get_value(instruction[1]), get_value(instruction[2]), 2):
								self.do_instructions(instruction[4])
						elif instruction[3] == '-':
							for i in xrange(get_value(instruction[1]), get_value(instruction[2]), -1):
								self.do_instructions(instruction[4])
						elif instruction[3] == '--':
							for i in xrange(get_value(instruction[1]), get_value(instruction[2]), -2):
								self.do_instructions(instruction[4])
				
				elif instruction[0] == 'while':
					while get_value(instruction[1]):
						self.do_instructions(instruction[2])
						
			except Exception as e:
            			logger.log('ERROR', 'Error executing instruction ' + str(instruction) + ': ' + str(e))

	
	def close_all(self):
		"""
		Close all connections and export har log
		"""

		if self.set_net_report:
			pprint(self.proxy.har['log']['entries'], self.complete_csv)
			self.complete_csv.close()
			logger.log('NOTE', 'Complete_net csv file exported to: ' + self.complete_csv.name)
		self.browser.close()
		self.proxy.close()
		self.server.stop()
		logger.log('NOTE', 'Connections closed')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-script", help="script file", required=True)
	parser.add_argument("-mode", help="compile/execution mode: -c (compile only) -x (execution only) -cx (compile & execution)", required=True)
	parser.add_argument("-debug", help="debug mode", required=False)
	args = parser.parse_args()
	script = args.script
	mode = args.mode
	debug = args.debug
    if debug == 'false':
        debug = False
    else:
        debug = True
	NavigationBot(script, mode, debug)


if __name__ == "__main__":
	try:
		sys.exit(main())
	except Exception as e:
		logger.log('ERROR', 'Printing traceback:\n' + traceback.format_exc())
		sys.exit(-1)
