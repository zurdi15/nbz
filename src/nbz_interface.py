#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import os
import psutil
import argparse
from pprint import pprint
from pyvirtualdisplay import Display
from nbz_core import NBZCore
from parser.nbz_parser import NBZParser
from data.natives import NATIVES
from lib.lib_log_nbz import Logging
logger = Logging()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

COLOURS = {'YELLOW': '\033[93m', 'RED': '\033[91m', 'NC': '\033[0m'}


class NBZInterface:
	"""Interface between all modules of the nbz.

	This class provides all the attributes needed to the core module, using the parser module
	to parse the nbz-script previously. After all script is executed, this class ends all connections.

	Attributes:
		core_attributes: dictionary of attributes needed for the core module

	Methods:
		compile_script
		close_all
	"""

	def __init__(self, script, script_parameters, proxy_enabled, debug):
		"""Init NBZInterface class with some attributes"""

		self.core_attributes = {
			'instruction_set': [],
			'variables': {},
			'NATIVES': NATIVES,
			'USER_FUNC': {},

			'script': script,
			'script_name': os.path.basename(script)[0:-4],
			'script_parameters': script_parameters,

			'browser': [],
			'proxy_enabled': proxy_enabled,

			'set_net_report': False,
			'net_reports_path': '',
			'complete_csv_path': '',
			'complete_csv': None,

			'debug': debug,
		}
		try:
			print("{YELLOW}  ############################ START NBZ ############################{NC}\n".format(YELLOW=COLOURS['YELLOW'],
																													NC=COLOURS['NC']))
			self.compile_script()
			nbz_core = NBZCore(self.core_attributes)
			nbz_core.execute_instructions()
			nbz_core.export_har_log()
			print("\n{YELLOW}  ############################ END NBZ ############################{NC}\n".format(YELLOW=COLOURS['YELLOW'],
																													NC=COLOURS['NC']))
		except Exception as e:
			logger.log('ERROR', str(e))
			print("\n{RED}  ************************ ERROR ENDING NBZ ************************{NC}\n".format(RED=COLOURS['RED'],
																												  NC=COLOURS['NC']))
		finally:
			self.close_all()

	def compile_script(self):
		"""Compile script to be executed.

		Returns:
			A lists structure with all the nbz-script converted
			A dict mapping variables of the script and their values
		"""

		try:
			z_code, z_code_vars = NBZParser(self.core_attributes['script'])
			self.core_attributes['instruction_set'] = z_code
			self.core_attributes['variables'] = z_code_vars
			if self.core_attributes['debug']:
				logger.log('NOTE', 'Instructions: {instructions}'.format(instructions=self.core_attributes['instruction_set']))
				logger.log('NOTE', 'Variables: {variables}'.format(variables=self.core_attributes['variables']))
		except Exception as e:
			logger.log('ERROR',
					   'Script not compiled ({script}): {exception}'.format(script=self.core_attributes['script'],
																			exception=e))

	def close_all(self):
		"""Close all connections"""

		logs_dir = os.path.join(BASE_DIR, "logs")
		if not os.path.exists(logs_dir):
			os.makedirs(logs_dir)
		logs = ['server.log', 'bmp.log', 'geckodriver.log', 'ghostdriver.log']
		for log in logs:
			if os.path.isfile(os.path.join(os.getcwd(), log)):
				os.rename(os.path.join(os.getcwd(), log), os.path.join(logs_dir, log))
		root_process = psutil.Process(os.getppid())
		root_children = root_process.children(recursive=True)[1:]
		for child in reversed(root_children):
			os.kill(child.pid, 9)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-script", help="script file", required=False)
	parser.add_argument("-script_parameters", help="script parameters", required=False, nargs='+')
	parser.add_argument("-display", help="enable display emulation", required=False)
	parser.add_argument("-resolution", help="set the screen emulator resolution", required=False)
	parser.add_argument("-proxy", help="enable proxy", required=False)
	parser.add_argument("-debug", help="debug mode", required=False)
	args = parser.parse_args()
	script = args.script
	script_parameters = args.script_parameters
	display = args.display
	resolution = args.resolution
	if display == 'true':
		if resolution != 'default':
			resolution = resolution.split('x')
			try:
				display = Display(visible=0, size=(resolution[0], resolution[1]))
			except IndexError:
				logger.log('ERROR', 'Error in resolution parameter. Must be like 1920x1080.')
				sys.exit(4)
		else:
			display = Display(visible=0, size=(2920, 1080))
		display.start()
	proxy_enabled = True if args.proxy == 'true' else False
	debug = True if args.debug == 'true' else False
	NBZInterface(script, script_parameters, proxy_enabled, debug)

if __name__ == "__main__":
	sys.exit(main())
