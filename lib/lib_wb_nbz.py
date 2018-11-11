#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import platform
import time

try:
	import urlparse
except ImportError:
	from urllib.parse import urlparse
from user_agents import USER_AGENTS
from lib_log_nbz import Logging

try:
	from selenium import webdriver
	from browsermobproxy import Server
except ImportError:
	raise Exception("Dependencies not installed. Please run install.sh")

logger = Logging()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class LibWb:
	"""Browser and proxy library.

	This class contains the methods to start the proxy and the native function to start the web browser.

	Methods:
		instance_browser
		get_driver_path
	"""

	def __init__(self):
		"""Init LibWb class"""

		pass

	def instance_browser(self, proxy_path, params):
		"""Start web browser and proxy server

		Args:
			proxy_path: path to the proxy binaries
			params: list of parameters
				-0: browser engine
				-1: user-agent
		Returns:
			Instance of the server, the proxy and the web browser
		"""

		try:
			server = Server(proxy_path)
			server.start()
		except Exception as e:
			raise Exception('Error launching server: {exception}'.format(exception=e))
		try:
			proxy = server.create_proxy()
		except RuntimeError:
			time.sleep(5)
			try:
				proxy = server.create_proxy()
			except Exception as e:
				raise Exception('Error configuring  proxy: {exception}'.format(exception=e))
		proxy.new_har()
		try:
			engine = params[0]
			driver_path = self.get_driver_path(engine)
			try:
				user_agent = USER_AGENTS[params[1]]
			except LookupError:
				user_agent = params[1]
		except LookupError:
			raise Exception('Function browser(): 2 arguments needed')
		try:
			logger.log('NOTE', 'Browser: {engine} (user-agent: {user_agent})'.format(engine=engine,
																							   user_agent=user_agent))
			try:
				proxy_url = urlparse.urlparse(proxy.proxy).path
			except AttributeError:
				proxy_url = urlparse(proxy.proxy).path
			if engine == 'chrome':
				ch_opt = webdriver.ChromeOptions()
				ch_opt.add_argument("--proxy-server=" + proxy_url)
				if user_agent != 'default':
					ch_opt.add_argument("--user-agent=" + user_agent)
				try:
					browser = webdriver.Chrome(executable_path=driver_path,
											   chrome_options=ch_opt)
				except LookupError:
					time.sleep(5)
					browser = webdriver.Chrome(executable_path=driver_path,
											   chrome_options=ch_opt)
			elif engine == 'firefox':
				ff_prf = webdriver.FirefoxProfile()
				if user_agent != 'default':
					ff_prf.set_preference("general.useragent.override", user_agent)
				try:
					browser = webdriver.Firefox(executable_path=driver_path,
												firefox_profile=ff_prf,
												proxy=proxy.selenium_proxy())
				except LookupError:
					time.sleep(5)
					browser = webdriver.Firefox(executable_path=driver_path,
												firefox_profile=ff_prf,
												proxy=proxy.selenium_proxy())
			elif engine == 'phantomjs':
				webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = user_agent
				service_args = ['--proxy={proxy}'.format(proxy=proxy_url),
								'--proxy-type=https']
				browser = webdriver.PhantomJS(driver_path, service_args=service_args)
			else:
				raise Exception('Not supported browser: {engine}'.format(engine=engine))
		except Exception as e:
			raise Exception('Error launching {engine} ({user_agent}): {exception}'.format(engine=engine,
																						  user_agent=user_agent,
																						  exception=e))
		return server, proxy, browser

	@staticmethod
	def get_driver_path(engine):
		"""Method to get the driver path for each engine and each operative system

		Args:
			engine: web browser to execute the nbz-script
		Returns:
			The driver path of the selected engine
		"""

		if engine == 'chrome':
			if platform.system() == 'Linux':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver')
			elif platform.system() == 'Windows':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver.exe')
			elif platform.system() == 'Darwin':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver_mac')
			else:
				raise Exception('Operative System not supported')
		elif engine == 'firefox':
			if os.name == 'posix':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'geckodriver')
			elif os.name == 'nt':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'geckodriver.exe')
			else:
				raise Exception('Operative System not supported')
		elif engine == 'phantomjs':
			if os.name == 'posix':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'phantomjs')
			elif os.name == 'nt':
				driver_path = os.path.join(BASE_DIR, 'drivers', 'phantomjs.exe')
			else:
				raise Exception('Operative System not supported')
		else:
			driver_path = ''
		return driver_path
