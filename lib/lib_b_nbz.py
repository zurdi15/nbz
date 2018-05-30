#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

import sys
import time
import unicodedata
from selenium.webdriver.common.keys import Keys
from lib_log_nbz import Logging
logger = Logging()


class LibB:


    def __init__(self):
        self.TIME = 0.5
        self.SPECIALS = {
            'ENTER': Keys.ENTER,
            'ESC': Keys.ESCAPE,
            'RETURN': Keys.RETURN,
            'TAB': Keys.TAB,
        }
        self.url_retries = 1
        self.url_retries_set = 1
        self.url_retries_wait_time = 0


    def set_url_retries(self, browser, params):
        """
        Defines url retries options
        """

        try:
            self.url_retries = params[0]
            self.url_retries_set = params[0]
            self.url_retries_wait_time = params[1]
        except Exception as e:
            logger.log('ERROR', 'Error setting get url retries: {exception}'.format(exception=e))
            sys.exit(-1)


    def get_url(self, browser, params):
        """
        Open given url
        """
   
        url = str(params[0])
   
        if self.url_retries > 0:
            try:
                logger.log('NOTE', 'Loading: {url}'.format(url=url))
                browser.get(url)
                self.url_retries = self.url_retries_set
            except Exception as e:
                logger.log('ERROR', 'Error loading url: {exception}'.format(exception=e))
                self.url_retries -= 1
                logger.log('ERROR', 'Error loading url, retries left: {url_retries}, waiting {time} seconds'.format(url_retries=self.url_retries, time=self.url_retries_wait_time))
                time.sleep(self.url_retries_wait_time)
                self.get_url(browser, params)
        else:
            logger.log('ERROR', 'Get url retries limit exceeded')
            sys.exit(-1)
    
    
    def fill_field(self, browser, params):
        """
        Fill given field with value and/or special-key
        """
    
        try:
            xpath = params[0]
            keys = params[1:]
        except LookupError:
            logger.log('ERROR', 'Function fill(): at least 2 arguments needed')
            sys.exit(-1)
    
        try:
            field = browser.find_element_by_xpath(xpath)
            for key in keys:
                key = str(key)
                if key in self.SPECIALS:
                    field.send_keys(self.SPECIALS[key])
                    if key == 'TAB':
                        field = browser.switch_to.active_element
                    logger.log('NOTE', 'Value: {key}'.format(key=key))
                else:
                    field.send_keys(key)
                    logger.log('NOTE', 'Value: {key}'.format(key=key))
                time.sleep(self.TIME)
        except Exception as e:
            logger.log('ERROR', 'Error with field {xpath): {exception}'.format(xpath=xpath, exception=e))
            sys.exit(-1)
    

    @staticmethod
    def clear_field(browser, params):
        """
        Clear given field
        """

        xpath = params[0]

        try:
            field = browser.find_element_by_xpath(xpath)
            field.clear()
            logger.log('NOTE', 'Field cleared')
        except Exception as e:
            logger.log('ERROR', 'Error with field {xpath}: {exception}'.format(xpath=xpath, exception=e))
            sys.exit(-1)
    
    
    def click_element(self, browser, params):
        """
        Click given element
        """

        xpath = params[0]

        try:
            element = browser.find_element_by_xpath(xpath)
            if element.text:
                logger.log('NOTE', 'Button clicked {text}'.format(text=element.text))
            elif element.get_attribute('value'):
                logger.log('NOTE', 'Button clicked {text}'.format(text=element.get_attribute('value')))
            else:
                logger.log('NOTE', 'Button clicked')
            element.click()
            time.sleep(self.TIME)
        except Exception as e:
            logger.log('ERROR', 'Error with button {xpath}: {exception}'.format(xpath=xpath, exception=e))
            sys.exit(-1)
    
    
    def select_option(self, browser, params):
        """
        Select an option from given selector
        """

        try:
            selector_xpath = params[0]
            option_xpath = params[1]
        except LookupError:
            logger.log('ERROR', 'Function select(): 2 arguments needed')
            sys.exit(-1)

        try:
            select = browser.find_element_by_xpath(selector_xpath)
            select.click()
            time.sleep(self.TIME)
            option = browser.find_element_by_xpath(option_xpath)
            logger.log('NOTE', 'Option selected {option}'.format(option=option.text))
            option.click()
            time.sleep(self.TIME)
        except Exception as e:
            logger.log('ERROR', 'Error with selector {selector_xpath}: {exception}'.format(selector_xpath=selector_xpath, exception=e))
            sys.exit(-1)
    

    @staticmethod
    def wait_time(browser, params):
        """
        Just wait given seconds
        """

        wait_time = params[0]

        try:
            logger.log('NOTE', 'Waiting {wait_time} seconds'.format(wait_time=wait_time))
            time.sleep(float(wait_time))
        except Exception as e:
            logger.log('ERROR', 'Error in explicit waiting: {exception}'.format(exception=e))
            sys.exit(-1)
    
    
    def back(self, browser, params):
        """
        Go back in browser history
        """
    
        try:
            browser.back()
            logger.log('NOTE', 'Going back')
            time.sleep(self.TIME)
        except Exception as e:
            logger.log('ERROR', 'Error going back: {exception}'.format(exception=e))
            sys.exit(-1)
    
    
    def forward(self, browser, params):
        """
        Go forward in browser history
        """
    
        try:
            browser.forward()
            logger.log('NOTE', 'Going forward')
            time.sleep(self.TIME)
        except Exception as e:
            logger.log('ERROR', 'Error going forward: {exception}'.format(exception=e))
            sys.exit(-1)
    

    @staticmethod
    def refresh(browser, params):
        """
        Refresh the page
        """
    
        try:
            browser.refresh()
            logger.log('NOTE', 'Refreshing...')
        except Exception as e:
            logger.log('ERROR', 'Error refreshing the web page: {exception}'.format(exception=e))
            sys.exit(-1)
    

    @staticmethod
    def get_text(browser, params):
        """
        Returns text from selected element
        """

        web_element = params[0]

        try:
            element = browser.find_element_by_xpath(web_element)
            logger.log('NOTE', 'Getting element: {web_element}'.format(web_element=web_element))
            return unicodedata.normalize('NFKD', element.text).encode('ascii','ignore')
        except Exception as e:
            logger.log('ERROR', 'Error with element {web_element}: {exception}'.format(web_element=web_element, exception=e))
            sys.exit(-1)
    

    @staticmethod
    def current_url(browser, params):
        """
        Returns current url
        """
    
        try:
            return browser.current_url
        except Exception as e:
            logger.log('ERROR', 'Error getting current url: {exception}'.format(exception=e))
            sys.exit(-1)
