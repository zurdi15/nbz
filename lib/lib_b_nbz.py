#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import time
import unicodedata
from selenium.webdriver.common.keys import Keys
from lib.lib_log_nbz import Logging

logger = Logging()


class LibB:
    """Basic library of native functions.

    This class contains all the basic functions to interact with the web browser.

    Attributes:
        TIME: internal time to wait between some kind of actions
        SPECIALS: dict of special characters of the keyboard
        url_retries_set: number of maximum retries to call an url
        url_retries: counter of retries to call an url
        url_retries_wait_time: time to wait between url retries
        url_retries_continute: continue if url fails

    Methods:
        set_url_retries
        get_url
        fill_field
        clear_field
        click_element
        select_option
        wait_time
        back
        forward
        refresh
        get_text
        current_url
    """

    def __init__(self):
        """Init LibB class with its attributes"""

        self.TIME = 0.5
        self.SPECIALS = {
            'ENTER': Keys.ENTER,
            'ESC': Keys.ESCAPE,
            'RETURN': Keys.RETURN,
            'TAB': Keys.TAB,
        }
        self.url_retries_set = 1
        self.url_retries = 1
        self.url_retries_wait_time = 0
        self.url_retries_continue = False

    def set_url_retries(self, browser, params):
        """Defines url retries options

        Args:
            browser: web browser instance
            params: list of parameters
                -0: number of maximum url retries
                -1: time to wait between url retries
        """

        try:
            self.url_retries = params[0]
            self.url_retries_set = params[0]
            self.url_retries_wait_time = params[1]
            self.url_retries_continue = params[2]
        except Exception:
            raise Exception('Error setting get url retries: 3 arguments needed')

    def get_url(self, browser, params):
        """Open an url

        Args:
            browser: web browser instance
            params: list of parameters
                -0: url to open
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
                logger.log('ERROR', 'Error loading url, retries left: {url_retries}, '
                                    'waiting {time} seconds'.format(url_retries=self.url_retries,
                                                                    time=self.url_retries_wait_time))
                time.sleep(self.url_retries_wait_time)
                self.get_url(browser, params)
        else:
            if self.url_retries_continue:
                self.url_retries = self.url_retries_set
            else:
                raise Exception('Get url retries limit exceeded')

    def fill_field(self, browser, params):
        """Fill a field with value and/or special-key

        Args:
            browser: web browser instance
            params: list of parameters
                -0: field xpath
                -1: string to fill with
        """

        try:
            xpath = params[0]
            keys = params[1:]
        except LookupError:
            raise Exception('Function fill(): at least 2 arguments needed')

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
            raise Exception('Error with field {xpath): {exception}'.format(xpath=xpath, exception=e))

    @staticmethod
    def clear_field(browser, params):
        """Clear a field

        Args:
            browser: web browser instance
            params: list of parameters
                -0: field xpath
        """

        xpath = params[0]
        try:
            field = browser.find_element_by_xpath(xpath)
            field.clear()
            logger.log('NOTE', 'Field cleared')
        except Exception as e:
            raise Exception('Error with field {xpath}: {exception}'.format(xpath=xpath,
                                                                           exception=e))

    def click_element(self, browser, params):
        """Click an element

        Args:
            browser: web browser instance
            params: list of parameters
                -0: element xpath
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
            raise Exception('Error with button {xpath}: {exception}'.format(xpath=xpath,
                                                                            exception=e))

    def select_option(self, browser, params):
        """Select an option from a selector

        Args:
            browser: web browser instance
            params: list of parameters
                -0: selector xpath
                -1: option xpath
        """

        try:
            selector_xpath = params[0]
            option_xpath = params[1]
        except LookupError:
            raise Exception('Function select(): 2 arguments needed')

        try:
            select = browser.find_element_by_xpath(selector_xpath)
            select.click()
            time.sleep(self.TIME)
            option = browser.find_element_by_xpath(option_xpath)
            logger.log('NOTE', 'Option selected {option}'.format(option=option.text))
            option.click()
            time.sleep(self.TIME)
        except Exception as e:
            raise Exception('Error with selector {selector_xpath}: '
                            '{exception}'.format(selector_xpath=selector_xpath,
                                                 exception=e))

    @staticmethod
    def wait_time(browser, params):
        """Just wait given seconds

        Args:
            browser: web browser instance
            params: list of parameters
                -0: seconds to wait
        """

        wait_time = params[0]
        try:
            logger.log('NOTE', 'Waiting {wait_time} seconds'.format(wait_time=wait_time))
            time.sleep(float(wait_time))
        except Exception as e:
            raise Exception('Error in explicit waiting: {exception}'.format(exception=e))

    def back(self, browser, params):
        """Go back in browser history

         Args:
            browser: web browser instance
            params: list of parameters (empty)
        """

        try:
            browser.back()
            logger.log('NOTE', 'Going back')
            time.sleep(self.TIME)
        except Exception as e:
            raise Exception('Error going back: {exception}'.format(exception=e))

    def forward(self, browser, params):
        """Go forward in browser history

        Args:
            browser: web browser instance
            params: list of parameters (empty)
        """

        try:
            browser.forward()
            logger.log('NOTE', 'Going forward')
            time.sleep(self.TIME)
        except Exception as e:
            raise Exception('Error going forward: {exception}'.format(exception=e))

    @staticmethod
    def refresh(browser, params):
        """Refresh the page

        Args:
            browser: web browser instance
            params: list of parameters (empty)
        """

        try:
            browser.refresh()
            logger.log('NOTE', 'Refreshing...')
        except Exception as e:
            raise Exception('Error refreshing the web page: {exception}'.format(exception=e))

    @staticmethod
    def get_text(browser, params):
        """Returns text from selected element

        Args:
            browser: web browser instance
            params: list of parameters
                -0: web element of which we want the text
        Returns:
            Plain text of the web element
        """

        web_element = params[0]
        try:
            element = browser.find_element_by_xpath(web_element)
            logger.log('NOTE', 'Getting element: {web_element}'.format(web_element=web_element))
            return unicodedata.normalize('NFKD', element.text).encode('ascii', 'ignore')
        except Exception as e:
            raise Exception('Error with element {web_element}: {exception}'.format(web_element=web_element,
                                                                                   exception=e))

    @staticmethod
    def current_url(browser, params):
        """Returns current url

        Args:
            browser: web browser instance
            params: list of parameters (empty)
        Returns:
            Current url
        """

        try:
            return browser.current_url
        except Exception as e:
            raise Exception('Error getting current url: {exception}'.format(exception=e))
