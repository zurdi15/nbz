#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

import sys
import time
import unicodedata
from selenium.webdriver.common.keys import Keys
from lib_logger import *
logger = Logging()


TIME_ = 0.5
SPECIALS = {
	'ENTER': Keys.ENTER,
	'ESC': Keys.ESCAPE,
	'RETURN': Keys.RETURN,
	'TAB': Keys.TAB,
}


def get_url(browser, params):
	"""
	Open given url
	"""

	try:
		logger.log('NOTE', 'Loading: ' + str(params[0]))
		browser.get(params[0])
	except Exception as e:
		logger.log('ERROR', 'Error loading url [' + str(params[0]) + '] - Invalid url?: ' + str(e))
		sys.exit(-1)


def fill_field(browser, params):
	"""
	Fill given field with value and/or special-key
	"""
    	
	try:
		box = browser.find_element_by_xpath(params[0])
		keys = iter(params) # Avoiding xpath in
		next(keys)	    # parameters list
		for key in keys:
			key = str(key) # Casting to str because z_code can have atirhmetic result as input parameter
			if key in SPECIALS:
				box.send_keys(SPECIALS[key])
				logger.log('NOTE', 'Value: ' + key)
			else:
				box.send_keys(key)
				logger.log('NOTE', 'Value: ' + key)
			time.sleep(TIME_)
	except Exception as e:
		logger.log('ERROR', 'Error with textbox ' + str(params) + ': ' + str(e))
		sys.exit(-1)


def clear_field(browser, params):
	"""
	Clear given field
	"""

	try:
		box = browser.find_element_by_xpath(params[0])
		box.clear()
		logger.log('NOTE', 'Textbox cleared')
	except Exception as e:
		logger.log('ERROR', 'Error with textbox ' + str(params) + ': ' + str(e))
		sys.exit(-1)


def click_element(browser, params):
	"""
	Click given element
	"""

	try:
		element = browser.find_element_by_xpath(params[0])
		element.click()
		if element.text:
			logger.log('NOTE', 'Button clicked ' + '[' + element.text + ']')
		elif element.get_attribute('value'):
			logger.log('NOTE', 'Button clicked ' + '[' + element.get_attribute('value') + ']')
		else:
			logger.log('NOTE', 'Button clicked')
			time.sleep(TIME_)
	except Exception as e:
		logger.log('ERROR', 'Error with button ' + str(params[0]) + ': ' + str(e))
		sys.exit(-1)


def select_option(browser, params):
	"""
	Select an option from given selector
	"""

	try:
		select = browser.find_element_by_xpath(params[0])
		select.click()
		time.sleep(TIME_)
		option = browser.find_element_by_xpath(params[1])
		option.click()
		logger.log('NOTE', 'Option selected ' + '[' + option.text + ']')
		time.sleep(TIME_)
	except Exception as e:
		logger.log('ERROR', 'Error with selector [' + str(params) + ']: ' + str(e))
		sys.exit(-1)


def wait_time(browser, params):
	"""
	Just wait given seconds
	"""
	
	try:
		logger.log('NOTE', 'Waiting ' + str(params) + ' seconds')
		time.sleep(float(params[0]))
	except Exception as e:
		logger.log('ERROR', 'Error in explicit waiting: ' + str(e))
		sys.exit(-1)


def back(browser, params):
	"""
	Go back in browser history
	"""

	try:
		browser.back()
		logger.log('NOTE', 'Going back')
		time.sleep(TIME_)
	except Exception as e:
		logger.log('ERROR', 'Error going back: ' + str(e))
		sys.exit(-1)


def forward(browser, params):
	"""
	Go forward in browser history
	"""

	try:
		browser.forward()
		logger.log('NOTE', 'Going forward')
		time.sleep(TIME_)
	except Exception as e:
		logger.log('ERROR', 'Error going forward: ' + str(e))
		sys.exit(-1)


def refresh(browser, params):
	"""
	Refresh the page
	"""

	try:
		browser.refresh()
		logger.log('NOTE', 'Refreshing...')
	except Exception as e:
		logger.log('ERROR', 'Error refreshing the web page')
		sys.exit(-1)


def get_text(browser, params):
	"""
	Returns text from selected element
	"""
	
	try:
		element = browser.find_element_by_xpath(params[0])
		logger.log('NOTE', 'Getting element: ' + params[0])
		return unicodedata.normalize('NFKD', element.text).encode('ascii','ignore')
	except Exception as e:
		logger.log('ERROR', 'Error with element ' + str(params) + ': ' + str(e))
		sys.exit(-1)


def current_url(browser, params):
	"""
	Returns current url
	"""

	try:
		return browser.current_url
	except Exception as e:
		logger.log('ERROR', 'Error getting current url: ' + str(e))
		sys.exit(-1)
