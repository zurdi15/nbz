#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Alejandro Atance>

import sys
import urlparse
from lib_logger import *
logger = Logging()
try:
	from selenium import webdriver
	from browsermobproxy import Server
except Exception:
	logger.log('ERROR', "Dependencies not installed. Please run install.sh")
	sys.exit(-1)
from user_agent import USER_AGENT_DICT


def start_proxy(proxy_path):
	"""
	Start proxy to capture net traffic
	"""

	logger.log('NOTE', 'Launching proxy server...')
	try:
		server = Server(proxy_path)
		server.start()
	except Exception as e:
		logger.log('ERROR', 'Error launching server: ' + str(e))
		sys.exit(-1)
	try:
		proxy = server.create_proxy()
		proxy.new_har()
	except Exception as e:
		logger.log('ERROR', 'Error configuring  proxy: ' + str(e))
		sys.exit(-1)
	return server, proxy


def instance_browser(proxy, params):
	"""
	Start web browser
	"""

	if len(params) < 2:
		logger.log('ERROR', 'Browser incorrectly defined, please check your script.')
		sys.exit(-1)
	else:
		try:
			try:
				user_agent = USER_AGENT_DICT[params[1]]
			except LookupError:
				user_agent = params[1]
			logger.log('NOTE', 'Launching Browser: ' + str(params[0]) + ' (user-agent = ' + str(params[1]) + ')...')
			if params[0] == 'chrome':
				ch_opt = webdriver.ChromeOptions()
				proxy_url = urlparse.urlparse(proxy.proxy).path
				ch_opt.add_argument("--proxy-server=" + proxy_url)
				try:
					ch_opt.add_argument("--user-agent=" + user_agent)
				except Exception:
					logger.log('ERROR', 'Not supported user-agent: ' + str(params[1]))
					sys.exit(-1)
				browser = webdriver.Chrome(chrome_options=ch_opt)
			elif params[0] == 'firefox':
				ff_prf = webdriver.FirefoxProfile()
				try:
					ff_prf.set_preference("general.useragent.override", user_agent)
				except Exception:
					logger.log('ERROR', 'Not supported user-agent: ' + str(params[1]))
					sys.exit(-1)
				browser = webdriver.Firefox(firefox_profile=ff_prf, proxy=proxy.selenium_proxy())
			else:
				logger.log('ERROR', 'Not supported browser: ' + params[0])
				sys.exit(-1)
		except Exception as e:
			logger.log('ERROR', 'Error launching ' + str(params[0]) + '(' + str(params[1]) + '): ' + str(e))
			sys.exit(-1)
		return browser
