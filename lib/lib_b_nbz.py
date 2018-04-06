#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

import sys
import time
import unicodedata
from selenium.webdriver.common.keys import Keys
from lib_log_nbz import *
logger = Logging()


class LibB:


    def __init__(self):
        TIME_ = 0.5
        SPECIALS = {
            'ENTER': Keys.ENTER,
            'ESC': Keys.ESCAPE,
            'RETURN': Keys.RETURN,
            'TAB': Keys.TAB,
        }
        self.url_retries = 1
        self.url_retries_set = 1
        self.url_retries_wait_time = 0


    def set_get_url_retries(self, browser, params):
        """
        Defines url retries options
        """

        try:
            self.url_retries = params[0]
            self.url_retries_set = params[0]
            self.url_retries_wait_time = params[1]
        except Exception as e:
            logger.log('ERROR', 'Error setting get url retries')
            sys.exit(-1)


    def get_url(self, browser, params):
        """
        Open given url
        """
   
        if self.url_retries > 0:
            try:
                logger.log('NOTE', 'Loading: ' + str(params[0]))
                browser.get(params[0])
                self.url_retries = self.url_retries_set
            except Exception as e:
                logger.log('ERROR', 'Error loading url [' + str(params[0]) + '] - (Invalid url?, Timeout?)')
                self.url_retries -= 1
                logger.log('ERROR', 'Error loading url, retries left: ' + str(self.url_retries) + ', waiting ' + str(self.url_retries_wait_time) + ' seconds')
                time.sleep(self.url_retries_wait_time)
                self.get_url(browser, params)
        else:
            logger.log('ERROR', 'Get url retries limit exceded')
            sys.exit(-1)
    
    
    def fill_field(self, browser, params):
        """
        Fill given field with value and/or special-key
        """
    
        try:
            box = browser.find_element_by_xpath(params[0])
            keys = params[1:]
            for key in keys:
                key = str(key)
                if key in SPECIALS:
                    box.send_keys(SPECIALS[key])
                    if key == 'TAB':
                        box = browser.switch_to.active_element
                    logger.log('NOTE', 'Value: ' + key)
                else:
                    box.send_keys(key)
                    logger.log('NOTE', 'Value: ' + key)
                time.sleep(TIME_)
        except Exception as e:
            logger.log('ERROR', 'Error with textbox ' + str(params) + ': ' + str(e))
            sys.exit(-1)
    
    
    def clear_field(self, browser, params):
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
    
    
    def click_element(self, browser, params):
        """
        Click given element
        """
    
        try:
            element = browser.find_element_by_xpath(params[0])
            if element.text:
                logger.log('NOTE', 'Button clicked ' + '[' + element.text + ']')
            elif element.get_attribute('value'):
                logger.log('NOTE', 'Button clicked ' + '[' + element.get_attribute('value') + ']')
            else:
                logger.log('NOTE', 'Button clicked')
            element.click()
            time.sleep(TIME_)
        except Exception as e:
            logger.log('ERROR', 'Error with button ' + str(params[0]) + ': ' + str(e))
            sys.exit(-1)
    
    
    def select_option(self, browser, params):
        """
        Select an option from given selector
        """
    
        try:
            select = browser.find_element_by_xpath(params[0])
            logger.log('NOTE', 'Option selected ' + '[' + option.text + ']')
            select.click()
            time.sleep(TIME_)
            option = browser.find_element_by_xpath(params[1])
            option.click()
            time.sleep(TIME_)
        except Exception as e:
            logger.log('ERROR', 'Error with selector [' + str(params) + ']: ' + str(e))
            sys.exit(-1)
    
    
    def wait_time(self, browser, params):
        """
        Just wait given seconds
        """
    
        try:
            logger.log('NOTE', 'Waiting ' + str(params) + ' seconds')
            time.sleep(float(params[0]))
        except Exception as e:
            logger.log('ERROR', 'Error in explicit waiting: ' + str(e))
            sys.exit(-1)
    
    
    def back(self, browser, params):
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
    
    
    def forward(self, browser, params):
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
    
    
    def refresh(self, browser, params):
        """
        Refresh the page
        """
    
        try:
            browser.refresh()
            logger.log('NOTE', 'Refreshing...')
        except Exception as e:
            logger.log('ERROR', 'Error refreshing the web page')
            sys.exit(-1)
    
    
    def get_text(self, browser, params):
        """
        Returns text from selected element
        """
    
        try:
            element = browser.find_element_by_xpath(params[0])
            logger.log('NOTE', 'Getting element: ' + str(params[0]))
            return unicodedata.normalize('NFKD', element.text).encode('ascii','ignore')
        except Exception as e:
            logger.log('ERROR', 'Error with element ' + str(params) + ': ' + str(e))
            sys.exit(-1)
    
    
    def current_url(self, browser, params):
        """
        Returns current url
        """
    
        try:
            return browser.current_url
        except Exception as e:
            logger.log('ERROR', 'Error getting current url: ' + str(e))
            sys.exit(-1)
