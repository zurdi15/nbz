#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
from pprint import pprint
from lib.lib_log_nbz import Logging

logger = Logging()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class LibSnf:
	"""Library of native sniffer functions

	This class contains all the sniffer functions to interact with the proxy

	Attributes:
		sniffer_attr: dict with all the values that can be get of a http call

	Methods:
		check_net
		check_net_parameters
		check_net_keywords
		net_report
		reset_har
	"""

	def __init__(self):
		"""Init LibSnf class with it attributes"""

		self.reset_attributes()

	def reset_attributes(self):
		self.sniffer_attr = {
			'request_ok': False,
			'url': '',
			'status_code': '404',
			'timestamp': '',
			'times': 0
		}

	def check_net(self, har, request):
		"""General method to select the way to check the HAR file

		Args:
			har: har proxy file
			request: some parameters which configure the check of a request
				-0: mode of checking (by parameters or by keyword)
		Returns:
			The value of the selected parameter of the request to check
		"""

		check_type = request[0]

		if check_type == 'params':
			return self.check_net_parameters(har, request)
		elif check_type == 'keyword':
			return self.check_net_keywords(har, request)
		else:
			raise Exception('Not admitted request type: {type}'.format(type=check_type))

	def check_net_parameters(self, har, request):
		"""Check if any request had the chosen parameters

		Args:
			har: har proxy file
			request: some parameters which configure the check of a request
				-1: parameter to return
				-2, -n: parameters of the url request
		Returns:
			Value of the parameter of the selected request
		"""

		try:
			attribute = request[1]
			params = request[2:]
		except LookupError:
			raise Exception('Function check_net(): at least 3 argument needed')

		for entry in har['log']['entries']:
			param_list_aux = entry['request']['url'].split('?')
			if len(param_list_aux) > 1:
				param_list = param_list_aux[1].split('&')
				if set(params).issubset(set(param_list)):
					if attribute == 'times':
						self.sniffer_attr['times'] += 1
					else:
						self.sniffer_attr['request_ok'] = True
						self.sniffer_attr['status_code'] = int(entry['response']['status'])
						self.sniffer_attr['url'] = entry['request']['url']
						self.sniffer_attr['timestamp'] = entry['startedDateTime'].replace('T', ' ')[:-10]
						break
		try:
			attribute = self.sniffer_attr[attribute]
			self.reset_attributes()
			return attribute
		except LookupError:
			raise Exception('Check_net() error: can\'t find {attribute} - '
							'invalid parameter to return'.format(attribute=attribute))

	def check_net_keywords(self, har, request):
		"""Check if any request had the chosen keyword

		Args:
			har: har proxy file
			request: some parameters which configure the check of a request
				-1: parameter to return
				-2: keyword to search
		Returns:
			Value of the parameter of the selected request
		"""

		attribute = request[1]
		keyword = request[2]

		for entry in har['log']['entries']:
			if entry['request']['url'].find(keyword) != -1:
				self.sniffer_attr['request_ok'] = True
				self.sniffer_attr['status_code'] = int(entry['response']['status'])
				self.sniffer_attr['url'] = entry['request']['url']
				self.sniffer_attr['timestamp'] = entry['startedDateTime'].replace('T', ' ')[:-10]
				break
		try:
			attribute = self.sniffer_attr[attribute]
			self.reset_attributes()
			return attribute
		except LookupError:
			raise Exception('Check_net() error: can\'t find {attribute} - '
							'invalid parameter to return'.format(attribute=attribute))

	@staticmethod
	def net_report(params, script_name):
		"""Create net report csv

		Args:
			params: list of parameters
				-0: file name
				-1: script name to build the path where the report will be stored
			script_name: name of the nbz script
		Returns:
			The report file opened in write mode
		"""
		file_name = params[0]

		net_reports_path = '{base_dir}/net_reports/{script_name}'.format(base_dir=os.path.abspath(\
																				  os.path.join(BASE_DIR,
																							   os.pardir)),
																			script_name=script_name)
		complete_csv_path = '{net_reports_path}/complete_net_log_{report_name}.csv'.format(
			net_reports_path=net_reports_path,
			report_name=file_name)
		if not os.path.exists(net_reports_path):
			os.makedirs(net_reports_path)
		return open(complete_csv_path, 'w')

	@staticmethod
	def reset_har(set_net_report, complete_csv, current_url, proxy):
		"""Reset proxy's HAR to check new requests

		Args:
			set_net_report: flag to know if the net report was requested by the user in the nbz-script
			complete_csv: file with the complete net report of the script
			current_url: current url of the browser
			proxy: instance of the proxy
		Returns:
			New instance of the har file of the proxy
		"""

		if set_net_report:
			complete_csv.write('URL: {url}\n\n'.format(url=current_url))
			pprint(proxy.har['log']['entries'], complete_csv)
		return proxy.new_har()
