#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import sys
import time
import datetime
from datetime import datetime
from random import randint
import re
from .lib_log_nbz import Logging

logger = Logging()


class LibA:
	"""Advanced library of native functions.

	This class contains all the advanced functions to interact with the web browser.

	Attributes:
		scroll: an integer where the actual scroll position of the web browser is stored

	Methods:
		print_
		random
		get_timestamp
		timestamp_diff
		open_file
		write_file
		write_table_as_csv
		close_file
		get_local_storage
		set_local_storage
		get_cookie
		set_cookie
		clear_cookies
		get_element
		children_num
		page_load_time
		scroll_down
		scroll_to_bottom
		scroll_up
		scroll_to_top
		execute_js
		set_timeout
		get_source_html
		export_source_html
		get_all_html_links
		get_element_html
		take_screenshot
		get_parameter
	"""

	def __init__(self):
		"""Init LibA class with scroll at top of the web page"""

		self.scroll = 0

	@staticmethod
	def print_(browser, params):
		"""Print string in terminal

		Args:
			browser: web browser instance
			params: list of parameters
				-0: string to be printed
		"""

		string = params[0]
		try:
			if string is None:
				logger.log('NOTE', '')
			else:
				logger.log('NOTE', string)
		except Exception as e:
			raise Exception('Error printing {string}: {exception}'.format(string=string, exception=e))

	@staticmethod
	def random(browser, params):
		"""Generate a random number between two numbers.

		Args:
			browser: web browser instance
			params: list of parameters
				-0: lower limit
				-1: higher limit
		Returns:
			Random number
		"""

		try:
			lower = params[0]
			higher = params[1]
		except LookupError:
			raise Exception('Function random(): 2 arguments needed')
		try:
			return randint(lower, higher)
		except Exception as e:
			raise Exception('Error getting random number: {exception}'.format(exception=e))

	@staticmethod
	def get_timestamp(browser, params):
		"""Get actual system timestamp

		Args:
			browser: web browser instance
			params: list of parameters
				-0: string time format (optional)
		Returns:
			Actual system timestamp string
		"""

		try:
			date_format = params[0]
		except:
			date_format = False
			logger.log('NOTE', 'Using default timestamp format')
		try:
			if not date_format:
				return str(datetime.now())[:-3]
			else:
				return time.strftime(date_format)
		except Exception as e:
			raise Exception('Error getting actual timestamp: {exception}'.format(exception=e))

	@staticmethod
	def timestamp_diff(browser, params):
		"""Return two timestamps difference

		Args:
			browser: web browser instance
			params: list of parameters
				-0: first timestamp
				-1: second timestamp
		Returns:
			Difference between first timestamp and second timestamp
		"""

		try:
			datetime_1 = params[0]
			datetime_2 = params[1]
		except LookupError:
			raise Exception('Function timestamp_diff(): 2 arguments needed')

		try:
			d1 = datetime.strptime(datetime_1, "%Y-%m-%d %H:%M:%S.%f")
			d2 = datetime.strptime(datetime_2, "%Y-%m-%d %H:%M:%S.%f")
			return (d1 - d2).total_seconds()
		except Exception as e:
			raise Exception('Error calculating date: {exception}'.format(exception=e))

	@staticmethod
	def open_file(browser, params):
		"""Open selected file in a variable

		Args:
			browser: web browser instance
			params: list of parameters
				-0: file name
				-1: open mode (read | write | append)
		Returns:
			File open in desired mode
		"""

		try:
			file_name = params[0]
			mode = params[1]
		except LookupError:
			raise Exception('Function open(): 2 arguments needed')

		try:
			return open(file_name, mode)
		except IOError:
			return open(file_name, "{}+".format(mode))
		except Exception as e:
			raise Exception('Error opening {file_name}: {exception}'.format(file_name=file_name,
																			exception=e))

	@staticmethod
	def write_file(browser, params):
		"""Write into selected file

		Args:
			browser: web browser instance
			params: list of parameters
				-0: file name
				-1: text to write into file
		"""

		try:
			file_name = params[0]
			text = params[1]
		except LookupError:
			raise Exception('Function write(): 2 arguments needed')

		try:
			sentences = text.split('\\n')
			for sent in sentences:
				file_name.write(sent + '\n')
		except Exception as e:
			raise Exception('Error writing {file_name}: {exception}'.format(file_name=file_name,
																			exception=e))

	@staticmethod
	def write_table_as_csv(browser, params):
		"""Write table as csv format

		Write a table from a web page into a csv file, adding some columns into the table if needed

		Args:
			browser: web browser instance
			params: list of parameters
				-0: table as web element (see getElement())
				-1: file to write in
				-2: csv delimiter
				-3: columns to add to the left
				-4: columns to add to the right
		"""

		try:
			table = params[0]
			file_ = params[1]
			delimiter = params[2]
			row_ = ''
			add_left = params[3]
			add_right = params[4]
		except LookupError:
			raise Exception('Function write_table_as_csv(): at least 3 arguments needed')

		try:
			for row in table.find_elements_by_tag_name('tr'):
				for cell in row.find_elements_by_tag_name('td'):
					row_ += cell.text + delimiter
				file_.write(add_left + row_ + add_right + '\n')
				row_ = ''
		except Exception as e:
			raise Exception('Error writing "' + str(params[1]) + '": {exception}'.format(exception=e))

	@staticmethod
	def close_file(browser, params):
		"""Close file

		Args:
			browser: web browser instance
			params: list of parameters
				-0: file name
		"""

		file_name = params[0]
		try:
			file_name.close()
		except Exception as e:
			raise Exception('Error closing {file_name}: {exception}'.format(file_name=file_name,
																			exception=e))

	@staticmethod
	def get_local_storage(browser, params):
		"""Returns selected item from local storage

		Args:
			browser: web browser instance
			params: list of parameters
				-0: item name
		Returns:
			The value of the item
		"""

		item = params[0]
		try:
			return browser.execute_script("return localStorage.getItem('{item}');".format(item=item))
		except Exception as e:
			raise Exception('Error getting {item} from local storage: {exception}'.format(item=item,
																						  exception=e))

	@staticmethod
	def set_local_storage(browser, params):
		"""Set selected value in selected item from local storage

		Args:
			browser: web browser instance
			params: list of parameters
				-0: item name
				-1: item value
		"""

		try:
			item = params[0]
			value = params[1]
		except LookupError:
			raise Exception('Function set_local_storage(): 2 arguments needed')

		try:
			browser.execute_script("localStorage.setItem('{item}', '{value}');".format(item=item,
																					   value=value))
			logger.log('NOTE', 'Setting local storage: {item}={value}'.format(item=item,
																			  value=value))
		except Exception as e:
			raise Exception('Error setting {value} in {item} of local storage: {exception}'.format(item=item,
																								   value=value,
																								   exception=e))

	@staticmethod
	def get_cookie(browser, params):
		"""Returns selected cookie

		Args:
			browser: web browser instance
			params: list of parameters
				-0: cookie name
		Returns:
			The value of the cookie
		"""

		cookie = params[0]
		try:
			return browser.get_cookie(cookie)['value']
		except LookupError:
			raise Exception('Error getting cookie {cookie}: Cookie not found'.format(cookie=cookie))

	@staticmethod
	def set_cookie(browser, params):
		"""Set value of cookie

		Args:
			browser: web browser instance
			params: list of parameters
				-0: cookie name
				-1: cookie value
		"""

		try:
			cookie = params[0]
			value = params[1]
		except LookupError:
			raise Exception('Function set_cookie(): 2 arguments needed')

		try:
			browser.add_cookie({'name': cookie, 'value': value})
			logger.log('NOTE', 'Setting cookie: {cookie}={value}'.format(cookie=cookie,
																		 value=value))
		except Exception as e:
			raise Exception('Error setting cookie {cookie} with {value}: {exception}'.format(cookie=cookie,
																							 value=value,
																							 exception=e))

	@staticmethod
	def clear_cookies(browser, params):
		"""Clear all cookies

		Args:
			browser: web browser instance
			params: list of parameters
				-0: cookie name
				-1: cookie value
		"""

		try:
			browser.delete_all_cookies()
			logger.log('NOTE', 'Deleting all cookies...')
		except Exception as e:
			raise Exception('Error deleting cookies: {exception}'.format(exception=e))

	@staticmethod
	def get_element(browser, params):
		"""Get element from web page as web-element

		Args:
			browser: web browser instance
			params: list of parameters
				-0: web element xpath
		Returns:
			Web element
		"""

		web_element = params[0]
		try:
			return browser.find_element_by_xpath(web_element)
		except Exception as e:
			raise Exception('Error searching element {web_element}: {exception}'.format(web_element=web_element,
																						exception=e))

	@staticmethod
	def children_num(browser, params):
		"""Returns the number of child elements of one element

		Args:
			browser: web browser instance
			params: list of parameters
				-0: web element
		Returns:
			Children of web element as integer number
		"""

		web_element = params[0]
		try:
			children = web_element.find_elements_by_xpath(".//*")
			return len(children)
		except Exception as e:
			raise Exception('Error getting element children: {exception}'.format(exception=e))

	@staticmethod
	def page_load_time(browser, params):
		"""Returns the load time of a web page

		Args:
			browser: web browser instance
			params: list of parameters (empty)
		"""

		try:
			return browser.execute_script('return performance.timing.loadEventEnd - '
										  'performance.timing.navigationStart;') / 1000.0
		except Exception as e:
			raise Exception('Error getting load page time: {exception}'.format(exception=e))

	def scroll_down(self, browser, params):
		"""Scroll down just screen height

		Args:
			browser: web browser instance
			params: list of parameters (empty)
		"""

		try:
			self.scroll += 1
			browser.execute_script("window.scrollTo(0, " + str(700 * self.scroll) + ");")
			logger.log('NOTE', 'Scrolling down')
		except Exception as e:
			raise Exception('Error scrolling down: {exception}'.format(exception=e))

	@staticmethod
	def scroll_to_bottom(browser, params):
		"""Scroll to the bottom of the web page

		Args:
			browser: web browser instance
			params: list of parameters (empty)
		"""

		try:
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			logger.log('NOTE', 'Scrolling down to bottom')
		except Exception as e:
			raise Exception('Error scrolling down: {exception}'.format(exception=e))

	def scroll_up(self, browser, params):
		"""Scroll up just screen height

		Args:
			browser: web browser instance
			params: list of parameters (empty)
		"""

		try:
			self.scroll -= 1
			browser.execute_script("window.scrollTo(0, " + str(700 * self.scroll) + ");")
			logger.log('NOTE', 'Scrolling up')
		except Exception as e:
			raise Exception('Error scrolling up: {exception}'.format(exception=e))

	@staticmethod
	def scroll_to_top(browser, params):
		"""Scroll to the top of the web page

		Args:
			browser: web browser instance
			params: list of parameters
		"""

		try:
			browser.execute_script("window.scrollTo(0, 0);")
			logger.log('NOTE', 'Scrolling up to top')
		except Exception as e:
			raise Exception('Error scrolling top: {exception}'.format(exception=e))

	@staticmethod
	def execute_js(browser, params):
		"""Execute any javascript instruction on the browser

		Args:
			browser: web browser instance
			params: list of parameters
				-0: javascript sentence
		"""

		script = params[0]
		try:
			logger.log('NOTE', 'Executing js: {script}'.format(script=script))
			return browser.execute_script(script)
		except Exception as e:
			raise Exception('Error executing js: {script}: {exception}'.format(script=script,
																			   exception=e))

	@staticmethod
	def set_timeout(browser, params):
		"""Set timeout at loading websites

		Args:
			browser: web browser instance
			params: list of parameters
				-0: time to wait until timeout (ms)
		"""

		timeout = params[0]
		try:
			browser.set_page_load_timeout(timeout)
			logger.log('NOTE', 'Timeout set to: {timeout}'.format(timeout=timeout))
		except Exception as e:
			raise Exception('Error setting timeout {exception}'.format(exception=e))

	@staticmethod
	def export_source_html(browser, params):
		"""Export html webpage into a file

		Args:
			browser: web browser instance
			params: list of parameters
				-0: file path where will be stored
		"""

		html_path = params[0]
		try:
			html = open('{html_path}'.format(html_path=html_path), 'w')
			html_text = browser.page_source
			html.write(html_text)
			html.close()
			logger.log('NOTE', 'HTML from {current_url} saved on: {html_path}'.format(current_url=browser.current_url,
																					  html_path=html_path))
		except Exception as e:
			raise Exception('Saving html source code: {exception}'.format(exception=e))

	@staticmethod
	def get_all_html_links(browser, params):
		"""Get all links from the page html

		Args:
			browser: web browser instance
			params: list of parameters (empty)
		Returns:
			A list of strings (links)
		"""

		try:
			html = browser.page_source
			links = re.findall('"((http)s?://.*?)"', html)
			all_links = []
			for link in links:
				if not link[0] in all_links:
					all_links.append(link[0])
			return all_links
		except Exception as e:
			raise Exception('Getting all html links: {exception}'.format(exception=e))

	@staticmethod
	def get_element_html(browser, params):
		"""Get html code from web element

		Args:
			browser: web browser instance
			params: list of parameters
				-0: web element xpath
		Returns:
			Html from web element
		"""

		web_element = params[0]
		try:
			element = browser.find_element_by_xpath(web_element)
			html = element.get_attribute('outerHTML')
			return html
		except Exception as e:
			raise Exception('Error getting html from {web_element}: {exception}'.format(web_element=web_element,
																						exception=e))

	@staticmethod
	def take_screenshot(browser, params):
		"""Takes a screenshot of the browser as .png

		Args:
			browser: web browser instance
			params: list of parameters
				-0: file path
		"""

		ss_path = params[0]
		try:
			browser.save_screenshot('{ss_path}'.format(ss_path=ss_path))
			logger.log('NOTE', 'Screenshot from {url} saved on: {ss_path}'.format(url=browser.current_url,
																				  ss_path=ss_path))
		except Exception as e:
			raise Exception('Error taking screenshot: {exception}'.format(exception=e))


	@staticmethod
	def wait_for_downloads(browser, params):
		"""Wait to all downloads to complete

		Args:
			browser: web browser instance
			params: list of parameters (empty)
		"""

		downloaded = False
		browser_name = browser.capabilities['browserName']

		def chrome_downloader(downloaded):
			browser.get('chrome://downloads')
			logger.log('NOTE', 'Waiting for downloads...')
			while not downloaded:
				for item in browser.find_elements_by_css_selector('body/deep/downloads-item'):
					if 'pause' in item.text.lower():
						time.sleep(2)
					else:
						downloaded = True

		def firefox_downloader(downloaded):
			logger.log('ERROR', 'Waiting for download not implemented with firefox')

		def phantomjs_downloader(downloaded):
			logger.log('ERROR', 'Waiting for download not implemented with phantomjs')

		downloader = {
			'chrome': chrome_downloader,
			'firefox': firefox_downloader,
			'phantomjs': phantomjs_downloader
		}

		try:
			downloader[browser_name](downloaded)
		except Exception as e:
			raise Exception('Error waiting for downloads: {exception}'.format(exception=e))


	@staticmethod
	def get_environment_variable(browser, params):
		"""Get an environment variable

		Args:
			browser: web browser instance
			params: list of parameters
				-0: environment variable name
		Returns:
			Value of the environment variable
		"""

		environment_variable = params[0]
		try:
			return os.environ.get(environment_variable)
		except Exception as e:
			raise Exception('Error getting environment variable: {exception}'.format(exception=e))

	@staticmethod
	def get_parameter(script_parameters, params):
		"""Get an environment variable

		Args:
			params: list of parameters
				-0: script parameter index
			script_parameters: list of script parameters
		Returns:
			Value of the script parameter
		"""

		script_parameter_index = params[0]

		try:
			return script_parameters[script_parameter_index]
		except IndexError:
			raise Exception('Error getting script parameter [{}]'.format(script_parameter_index))
