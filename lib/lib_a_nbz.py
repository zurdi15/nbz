#!/usr/bin/python
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


def print_(browser, params):
    """
    Print string
    """

    try:
        if params[0] == None:
            logger.log('NOTE', '')
        else:
            logger.log('NOTE', str(params[0]))
    except Exception as e:
        logger.log('ERROR', 'Error printing "' + str(params) + '": ' + str(e))
        sys.exit(-1)


def random(browser, params):
    """
    Return randome number
    """

    try:
        return randint(params[0], params[1])
    except Exception as e:
        logger.log('ERROR', 'Error getting random number: ' + str(e))
        sys.exit(-1)


def get_timestamp(browser, params):
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


def timestamp_diff(browser, params):
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


def open_file(browser, params):
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


def write_file(browser, params):
    """
    Write in selected file
    """

    try:
        sentences = params[1].split('\\n')
        for sent in sentences:
            sent = unicode(sent)
            fixed_sent = unicodedata.normalize('NFKD', sent).encode('ascii', 'ignore')
            params[0].write(fixed_sent)
            params[0].write('\n')
    except Exception as e:
        logger.log('ERROR', 'Error writing "' + str(params[0]) + '": ' + str(e))
        sys.exit(-1)


def write_table_as_csv(browser, params):
    """
    Write table as csv format
    """

    try:
        if not os.path.exists(params[1]):
            os.makedirs(params[1])
        file_ = params[1]
        delimiter = params[2]
        row_ = ''
        if len(params) == 4:
            add = params[3]
        else:
            add = ''
        for row in params[0].find_elements_by_tag_name('tr'):
            for cell in row.find_elements_by_tag_name('td'):
                row_ += unicodedata.normalize('NFKD', cell.text).encode('ascii', 'ignore') + delimiter
                row_ = add + row_ + '\n'
            file_.write(row_)
            row_ = ''
    except Exception as e:
        logger.log('ERROR', 'Error writing "' + str(params[0]) + '": ' + str(e))
        sys.exit(-1)


def close_file(browser, params):
    """
    Close selected file
    """

    try:
        params[0].close()
    except Exception as e:
        logger.log('ERROR', 'Error closing "' + str(params[0]) + '": ' + str(e))
        sys.exit(-1)


def get_local_storage(browser, params):
    """
    Returns selected item from local storage 
    """

    try:
        return browser.execute_script("return localStorage.getItem('" + params[0] + "');")
    except Exception as e:
        logger.log('ERROR', 'Error getting "' + str(params[0]) + '" from local storage: ' + str(e))
        sys.exit(-1)


def set_local_storage(browser, params):
    """
    Set selected value in selected item from local storage
    """

    try:
        browser.execute_script("localStorage.setItem('" + params[0] + "', '" + params[1] + "');")
        logger.log('NOTE', 'Setting local storage: ' + params[0] + '="' + params[1] + '"')
    except Exception as e:
        logger.log('ERROR', 'Error setting "' + str(params[1]) + '" in "' + str(params[0]) + '" of local storage: ' + str(e))
        sys.exit(-1)


def get_cookie(browser, params):
    """
    Returns selected cookie
    """

    try:
        return browser.get_cookie(params[0])['value']
    except Exception as e:
        logger.log('ERROR', 'Error getting cookie "' + params[0] + '": ' + str(e))
        sys.exit(-1)


def set_cookie(browser, params):
    """
    Set value on cookie
    """

    try:
        browser.add_cookie({'name' : params[0], 'value' : params[1]})
        logger.log('NOTE', 'Setting cookie: ' + str(params[0]) + '="' + str(params[1]) + '"')
    except Exception as e:
        logger.log('ERROR', 'Error setting cookie "' + str(params[0]) + '" with "' + str(params[1]) + '": ' + str(e))
        sys.exit(-1)


def get_element(browser, params):
    """
    Get element from web page
    """

    try:
        return browser.find_element_by_xpath(params[0])
    except Exception as e:
        logger.log('ERROR', 'Error searching element ' + str(params[0]) + ': ' + str(e))
        sys.exit(-1)


def children_num(browser, params):
    """
    Returns the number of child elements of one element
    """

    try:
        children = params[0].find_elements_by_xpath(".//*")
        return len(children)
    except Exception as e:
        logger.log('ERROR', 'Error gerring element children')
        sys.exit(-1)


def page_load_time(browser, params):
    """
    Returns load page time
    """

    try:
        return browser.execute_script('return performance.timing.loadEventEnd - performance.timing.navigationStart;')
    except Exception as e:
        logger.log('ERROR', 'Error getting load page time: ' + str(e))
        sys.exit(-1)


def scroll_to_bottom(browser, params):
    """
    Scroll to the bottom of the web page
    """

    try:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.log('NOTE', 'Scrolling down to bottom')
    except Exception as e:
        logger.log('ERROR', 'Error scrolling down: ' + str(e))
        sys.exit(-1)


def scroll_to_top(browser, params):
    """
    Scroll to the top of the web page
    """

    try:
        browser.execute_script("window.scrollTo(0, 0);")
        logger.log('NOTE', 'Scrolling up to top')
    except Exception as e:
        logger.log('ERROR', 'Error scrolling top: ' + str(e))
        sys.exit(-1)


def execute_js(browser, params):
    """
    Execute any instruction in javascript on the browser
    """

    try:
        logger.log('NOTE', 'Executing js: ' + params[0])
        return browser.execute_script(params[0])
    except Exception as e:
        logger.log('ERROR', 'Error executing js: ' + params[0] + ': ' + str(e))
        sys.exit(-1)


def set_timeout(browser, params):
    """
    Set timeout at loading webpages
    """

    try:
        browser.set_page_load_timeout(params[0])
        logger.log('NOTE', 'Timeout set to: ' + str(params[0]))
    except Exception as e:
        logger.log('ERROR', 'Error setting timeout ' + str(e))


def get_html(browser, params):
    """
    Get html web page
    """

    try:
        if not os.path.exists(params[0]):
            os.makedirs(params[0])
        html_path = params[0]
        html = open(html_path + '/' + str(params[1]) + '.html', 'w')
        fixed_html = unicodedata.normalize('NFKD', browser.page_source).encode('ascii','ignore')
        html.write(fixed_html)
        html.close()
        logger.log('NOTE', 'HTML from ' + browser.current_url + ' saved on: ' + html_path + '/' + str(params[1]) + '.html')
    except Exception as e:
        logger.log('ERROR', 'Saving html source: ' + str(e))
        sys.exit(-1)


def get_element_html(browser, params):
    """
    Get html code from web element
    """

    try:
        element = browser.find_element_by_xpath(params[0])
        fixed_element_html = unicodedata.normalize('NFKD', element.get_attribute('outerHTML')).encode('ascii', 'ignore')
        return fixed_element_html
    except Exception as e:
        logger.log('ERROR', 'Error getting html from [' + str(params[0] + ']: ' + str(e)))
        sys.exit(-1)


def take_screenshot(browser, params):
    """
    Takes a screenshot of the browser
    """

    try:
        if not os.path.exists(params[0]):
            os.makedirs(params[0])
        ss_path = params[0]
        browser.save_screenshot(ss_path + '/' + params[1] + '.png')
        logger.log('NOTE', 'Screenshot from ' + browser.current_url + ' saved on: ' + ss_path + '/' + str(params[1]) + '.png')
    except Exception as e:
        logger.log('ERROR', 'Error taking screenshot: ' + str(e))
        sys.exit(-1)