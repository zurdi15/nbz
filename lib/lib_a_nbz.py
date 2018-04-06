#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import os
import time
from datetime import datetime
from random import randint
import unicodedata
from lib_log_nbz import *
logger = Logging()


class LibA:

    def __init__(self):
        self.scroll = 0


    def print_(self, browser, params):
        """
        Print string
        """
    
        try:
            if params[0] == None:
                logger.log('NOTE', '')
            else:
                logger.log('NOTE', str(params[0]))
        except Exception as e:
            logger.log('ERROR', 'Error printing "' + str(params[0]) + '": ' + str(e))
            sys.exit(-1)
    
    
    def random(self, browser, params):
        """
        Return randome number
        """
    
        try:
            return randint(params[0], params[1])
        except Exception as e:
            logger.log('ERROR', 'Error getting random number: ' + str(e))
            sys.exit(-1)
    
    
    def get_timestamp(self, browser, params):
        """
        Return actual system timestamp
        """
    
        try:
            if not params[0]:
                return time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return time.strftime(params[0])
        except Exception as e:
            logger.log('ERROR', 'Error getting actual timestamp: ' + str(e))
            sys.exit(-1)
    
    
    def timestamp_diff(self, browser, params):
        """
        Return timestamps difference
        """
    
        try:
            d1 = datetime.strptime(params[0], "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(params[1], "%Y-%m-%d %H:%M:%S")
            return d1 - d2
        except Exception as e:
            logger.log('ERROR', 'Error substracting dates: ' + str(e))
            sys.exit(-1)
    
    
    def open_file(self, browser, params):
        """
        Open selected file in a variable
        """
    
        try:
            if len(params) < 2:
                logger.log('ERROR', 'Error opening ' + str(params[0]) + ' open mode needed')
                sys.exit(-1)
            else:
                return open(params[0], params[1])
        except Exception as e:
            logger.log('ERROR', 'Error opening "' + str(params[0]) + '": ' + str(e))
            sys.exit(-1)
    
    
    def write_file(self, browser, params):
        """
        Write in selected file
        """
    
        try:
            file_ = params[0]
     	    try:
                sentences = params[1].split('\\n')
            except:
                sentences = params[1]
            for sent in sentences:
                if isinstance(sent, unicode):
                    file_.write(sent.encode('utf-8') + '\n')
                else:
                    file_.write(sent + '\n')
        except Exception as e:
            logger.log('ERROR', 'Error writing "' + str(params[0]) + '": ' + str(e))
            sys.exit(-1)
    
    
    def write_table_as_csv(self, browser, params):
        """
        Write table as csv format
        """
    
        try:
            table = params[0]
            file_ = params[1]
            delimiter = params[2]
            row_ = ''
            if len(params) == 4:
                add = params[3]
            else:
                add = ''
            for row in params[0].find_elements_by_tag_name('tr'):
                for cell in row.find_elements_by_tag_name('td'):
                    if isinstance(cell.text, unicode):
                        row_ += cell.text.encode('utf-8') + delimiter
                    else:
                        row_ += cell.text + delimiter
                file_.write(add + row_+ '\n')
                row_ = ''
    
    
        except Exception as e:
            logger.log('ERROR', 'Error writing "' + str(params[1]) + '": ' + str(e))
            sys.exit(-1)
    
    
    def close_file(self, browser, params):
        """
        Close selected file
        """
    
        try:
            params[0].close()
        except Exception as e:
            logger.log('ERROR', 'Error closing "' + str(params[0]) + '": ' + str(e))
            sys.exit(-1)
    
    
    def get_local_storage(self, browser, params):
        """
        Returns selected item from local storage 
        """
    
        try:
            return browser.execute_script("return localStorage.getItem('" + params[0] + "');")
        except Exception as e:
            logger.log('ERROR', 'Error getting "' + str(params[0]) + '" from local storage: ' + str(e))
            sys.exit(-1)
    
    
    def set_local_storage(self, browser, params):
        """
        Set selected value in selected item from local storage
        """
    
        try:
            browser.execute_script("localStorage.setItem('" + params[0] + "', '" + params[1] + "');")
            logger.log('NOTE', 'Setting local storage: ' + params[0] + '="' + params[1] + '"')
        except Exception as e:
            logger.log('ERROR', 'Error setting "' + str(params[1]) + '" in "' + str(params[0]) + '" of local storage: ' + str(e))
            sys.exit(-1)
    
    
    def get_cookie(self, browser, params):
        """
        Returns selected cookie
        """
    
        try:
            return browser.get_cookie(params[0])['value']
        except Exception as e:
            logger.log('ERROR', 'Error getting cookie "' + params[0] + '": ' + str(e))
            sys.exit(-1)
    
    
    def set_cookie(self, browser, params):
        """
        Set value on cookie
        """
    
        try:
            browser.add_cookie({'name' : params[0], 'value' : params[1]})
            logger.log('NOTE', 'Setting cookie: ' + str(params[0]) + '="' + str(params[1]) + '"')
        except Exception as e:
            logger.log('ERROR', 'Error setting cookie "' + str(params[0]) + '" with "' + str(params[1]) + '": ' + str(e))
            sys.exit(-1)
    
    
    def get_element(self, browser, params):
        """
        Get element from web page
        """
    
        try:
            return browser.find_element_by_xpath(params[0])
        except Exception as e:
            logger.log('ERROR', 'Error searching element ' + str(params[0]) + ': ' + str(e))
            sys.exit(-1)
    
    
    def children_num(self, browser, params):
        """
        Returns the number of child elements of one element
        """
    
        try:
            children = params[0].find_elements_by_xpath(".//*")
            return len(children)
        except Exception as e:
            logger.log('ERROR', 'Error gerring element children')
            sys.exit(-1)
    
    
    def page_load_time(self, browser, params):
        """
        Returns load page time
        """
    
        try:
            return browser.execute_script('return performance.timing.loadEventEnd - performance.timing.navigationStart;') / 1000.0
        except Exception as e:
            logger.log('ERROR', 'Error getting load page time: ' + str(e))
            sys.exit(-1)
    
    
    def scroll_down(self, browser, params):
        """
        Scroll down just screen height
        """

        try:
            self.scroll += 1
            browser.execute_script("window.scrollTo(0, "+str(700*self.scroll)+");")
            logger.log('NOTE', 'Scrolling down')
        except Exception as e:
            logger.log('ERROR', 'Error scrolling down: ' + str(e))
            sys.exit(-1)


    def scroll_to_bottom(self, browser, params):
        """
        Scroll to the bottom of the web page
        """
    
        try:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.log('NOTE', 'Scrolling down to bottom')
        except Exception as e:
            logger.log('ERROR', 'Error scrolling down: ' + str(e))
            sys.exit(-1)
    
    
    def scroll_up(self, browser, params):
        """
        Scroll up just screen height
        """

        try:
            self.scroll -= 1
            browser.execute_script("window.scrollTo(0, "+str(700*self.scroll)+");")
            logger.log('NOTE', 'Scrolling up')
        except Exception as e:
            logger.log('ERROR', 'Error scrolling up: ' + str(e))
            sys.exit(-1)


    def scroll_to_top(self, browser, params):
        """
        Scroll to the top of the web page
        """
    
        try:
            browser.execute_script("window.scrollTo(0, 0);")
            logger.log('NOTE', 'Scrolling up to top')
        except Exception as e:
            logger.log('ERROR', 'Error scrolling top: ' + str(e))
            sys.exit(-1)
    
    
    def execute_js(self, browser, params):
        """
        Execute any instruction in javascript on the browser
        """
    
        try:
            logger.log('NOTE', 'Executing js: ' + params[0])
            return browser.execute_script(params[0])
        except Exception as e:
            logger.log('ERROR', 'Error executing js: ' + params[0] + ': ' + str(e))
            sys.exit(-1)
    
    
    def set_timeout(self, browser, params):
        """
        Set timeout at loading webpages
        """
    
        try:
            browser.set_page_load_timeout(params[0])
            logger.log('NOTE', 'Timeout set to: ' + str(params[0]))
        except Exception as e:
            logger.log('ERROR', 'Error setting timeout ' + str(e))
    
    
    def get_html(self, browser, params):
        """
        Get html web page
        """
    
        try:
            html_path = params[0]
            html = open(html_path + '/' + str(params[1]) + '.html', 'w')
            html_text = browser.page_source
            if isinstance(html_text, unicode):
                html.write(html_text.encode('utf-8'))
            else:
                html.write(html_text)
            html.close()
            logger.log('NOTE', 'HTML from ' + browser.current_url + ' saved on: ' + html_path + '/' + str(params[1]) + '.html')
        except Exception as e:
            logger.log('ERROR', 'Saving html source: ' + str(e))
            sys.exit(-1)
    
    
    def get_element_html(self, browser, params):
        """
        Get html code from web element
        """
    
        try:
            element = browser.find_element_by_xpath(params[0])
            html = element.get_attribute('outerHTML')
            if isinstance(html, unicode):
                return html.encode('utf-8')
            else:
                return html
        except Exception as e:
            logger.log('ERROR', 'Error getting html from [' + str(params[0] + ']: ' + str(e)))
            sys.exit(-1)
    
    
    def take_screenshot(self, browser, params):
        """
        Takes a screenshot of the browser
        """
    
        try:
            ss_path = params[0]
            browser.save_screenshot(ss_path + '/' + params[1] + '.png')
            logger.log('NOTE', 'Screenshot from ' + browser.current_url + ' saved on: ' + ss_path + '/' + str(params[1]) + '.png')
        except Exception as e:
            logger.log('ERROR', 'Error taking screenshot: ' + str(e))
            sys.exit(-1)
