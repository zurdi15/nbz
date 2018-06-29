#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import time
from datetime import datetime
from random import randint
from lib_log_nbz import Logging
logger = Logging()


class LibA:

    def __init__(self):
        self.scroll = 0


    @staticmethod
    def print_(browser, params):
        """
        Print string
        """

        string = str(params[0])

        try:
            if string is None:
                logger.log('NOTE', '')
            else:
                logger.log('NOTE', string)
        except Exception as e:
            logger.log('ERROR', 'Error printing {string}: {exception}'.format(string=string, exception=e))
            sys.exit(-1)


    @staticmethod
    def random(browser, params):
        """
        Return random number
        """

        try:
            lower = params[0]
            higher = params[1]
        except LookupError:
            logger.log('ERROR', 'Function random(): 2 arguments needed')
            sys.exit(-1)

        try:
            return randint(lower, higher)
        except Exception as e:
            logger.log('ERROR', 'Error getting random number: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def get_timestamp(browser, params):
        """
        Return actual system timestamp
        """

        date_format = params[0]

        try:
            if not date_format:
                return time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return time.strftime(date_format)
        except Exception as e:
            logger.log('ERROR', 'Error getting actual timestamp: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def timestamp_diff(browser, params):
        """
        Return timestamps difference
        """

        try:
            datetime_1 = params[0]
            datetime_2 = params[1]
        except LookupError:
            logger.log('ERROR', 'Function timestamp_diff(): 2 arguments needed')
            sys.exit(-1)

        try:
            d1 = datetime.strptime(datetime_1, "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(datetime_2, "%Y-%m-%d %H:%M:%S")
            return d1 - d2
        except Exception as e:
            logger.log('ERROR', 'Error calculating date: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def open_file(browser, params):
        """
        Open selected file in a variable
        """

        try:
            file_name = params[0]
            mode = params[1]
        except LookupError:
            logger.log('ERROR', 'Function open(): 2 arguments needed')
            sys.exit(-1)

        try:
            return open(file_name, mode)
        except Exception as e:
            logger.log('ERROR', 'Error opening {file_name}: {exception}'.format(file_name=file_name, exception=e))
            sys.exit(-1)


    @staticmethod
    def write_file(browser, params):
        """
        Write in selected file
        """

        try:
            file_name = params[0]
            text = params[1]
        except LookupError:
            logger.log('ERROR', 'Function write(): 2 arguments needed')
            sys.exit(-1)

        try:
            sentences = text.split('\\n')
            for sent in sentences:
                if isinstance(sent, unicode):
                    file_name.write(sent.encode('utf-8') + '\n')
                else:
                    file_name.write(sent + '\n')
        except Exception as e:
            logger.log('ERROR', 'Error writing {file_name}: {exception}'.format(file_name=file_name, exception=e))
            sys.exit(-1)


    @staticmethod
    def write_table_as_csv(browser, params):
        """
        Write table as csv format
        """


        try:
            table = params[0]
            file_ = params[1]
            delimiter = params[2]
            row_ = ''
            add_left = params[3]
            add_right = params[4]
        except LookupError:
            logger.log('ERROR', 'Function write_table_as_csv(): at least 3 arguments needed')
            sys.exit(-1)

        try:
            for row in table.find_elements_by_tag_name('tr'):
                for cell in row.find_elements_by_tag_name('td'):
                    if isinstance(cell.text, unicode):
                        row_ += cell.text.encode('utf-8') + delimiter
                    else:
                        row_ += cell.text + delimiter
                file_.write(add_left + row_+ add_right + '\n')
                row_ = ''
        except Exception as e:
            logger.log('ERROR', 'Error writing "' + str(params[1]) + '": {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def close_file(browser, params):
        """
        Close selected file
        """

        file_name = params[0]

        try:
            file_name.close()
        except Exception as e:
            logger.log('ERROR', 'Error closing {file_name}: {exception}'.format(file_name=file_name, exception=e))
            sys.exit(-1)


    @staticmethod
    def get_local_storage(browser, params):
        """
        Returns selected item from local storage
        """

        item = params[0]

        try:
            return browser.execute_script("return localStorage.getItem('{item}');".format(item=item))
        except Exception as e:
            logger.log('ERROR', 'Error getting {item} from local storage: {exception}'.format(item=item, exception=e))
            sys.exit(-1)


    @staticmethod
    def set_local_storage(browser, params):
        """
        Set selected value in selected item from local storage
        """

        try:
            item = params[0]
            value = params[1]
        except LookupError:
            logger.log('ERROR', 'Function set_local_storage(): 2 arguments needed')
            sys.exit(-1)

        try:
            browser.execute_script("localStorage.setItem('{item}', '{value}');".format(item=item, value=value))
            logger.log('NOTE', 'Setting local storage: {item}={value}'.format(item=item, value=value))
        except Exception as e:
            logger.log('ERROR', 'Error setting {value} in {item} of local storage: {exception}'.format(item=item, value=value, exception=e))
            sys.exit(-1)


    @staticmethod
    def get_cookie(browser, params):
        """
        Returns selected cookie
        """

        cookie = params[0]

        try:
            return browser.get_cookie(cookie)['value']
        except LookupError:
            logger.log('ERROR', 'Error getting cookie {cookie}: Cookie not found'.format(cookie=cookie))
            sys.exit(-1)


    @staticmethod
    def set_cookie(browser, params):
        """
        Set value on cookie
        """

        try:
            cookie = params[0]
            value = params[1]
        except LookupError:
            logger.log('ERROR', 'Function set_cookie(): 2 arguments needed')
            sys.exit(-1)

        try:
            browser.add_cookie({'name' : cookie, 'value' : value})
            logger.log('NOTE', 'Setting cookie: {cookie}={value}'.format(cookie=cookie, value=value))
        except Exception as e:
            logger.log('ERROR', 'Error setting cookie {cookie} with {value}: {exception}'.format(cookie=cookie, value=value, exception=e))
            sys.exit(-1)


    @staticmethod
    def get_element(browser, params):
        """
        Get element from web page
        """

        web_element = params[0]

        try:
            return browser.find_element_by_xpath(web_element)
        except Exception as e:
            logger.log('ERROR', 'Error searching element {web_element}: {exception}'.format(web_element=web_element, exception=e))
            sys.exit(-1)


    @staticmethod
    def children_num(browser, params):
        """
        Returns the number of child elements of one element
        """

        web_element = params[0]

        try:
            children = web_element.find_elements_by_xpath(".//*")
            return len(children)
        except Exception as e:
            logger.log('ERROR', 'Error getting element children: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def page_load_time(browser, params):
        """
        Returns load page time
        """

        try:
            return browser.execute_script('return performance.timing.loadEventEnd - performance.timing.navigationStart;') / 1000.0
        except Exception as e:
            logger.log('ERROR', 'Error getting load page time: {exception}'.format(exception=e))
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
            logger.log('ERROR', 'Error scrolling down: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def scroll_to_bottom(browser, params):
        """
        Scroll to the bottom of the web page
        """

        try:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.log('NOTE', 'Scrolling down to bottom')
        except Exception as e:
            logger.log('ERROR', 'Error scrolling down: {exception}'.format(exception=e))
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
            logger.log('ERROR', 'Error scrolling up: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def scroll_to_top(browser, params):
        """
        Scroll to the top of the web page
        """

        try:
            browser.execute_script("window.scrollTo(0, 0);")
            logger.log('NOTE', 'Scrolling up to top')
        except Exception as e:
            logger.log('ERROR', 'Error scrolling top: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def execute_js(browser, params):
        """
        Execute any instruction in javascript on the browser
        """

        script = params[0]

        try:
            logger.log('NOTE', 'Executing js: {script}'.format(script=script))
            return browser.execute_script(script)
        except Exception as e:
            logger.log('ERROR', 'Error executing js: {script}: {exception}'.format(script=script, exception=e))
            sys.exit(-1)


    @staticmethod
    def set_timeout(browser, params):
        """
        Set timeout at loading webpages
        """

        timeout = params[0]

        try:
            browser.set_page_load_timeout(timeout)
            logger.log('NOTE', 'Timeout set to: {timeout}'.format(timeout=timeout))
        except Exception as e:
            logger.log('ERROR', 'Error setting timeout {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def export_html(browser, params):
	"""
        Get html webpage
        """

	try:
            html_path = params[0]
            html_name = params[1]
        except LookupError:
            logger.log('ERROR', 'Function export_html(): 2 arguments needed')
            sys.exit(-1)

        try:
            html = open('{html_path}/{html_name}.html'.format(html_path=html_path, html_name=html_name), 'w')
            html_text = browser.page_source
            if isinstance(html_text, unicode):
                html.write(html_text.encode('utf-8'))
            else:
                html.write(html_text)
            html.close()
            logger.log('NOTE', 'HTML from {current_url} saved on: {html_path}/{html_name}.html'.format(current_url=browser.current_url, html_path=html_path, html_name=html_name))
        except Exception as e:
            logger.log('ERROR', 'Saving html source: {exception}'.format(exception=e))
            sys.exit(-1)


    @staticmethod
    def get_all_html_links(browser):
	"""
        Get all links from the page html
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
	    logger.log('ERROR', 'Getting all html links: {exception}'.format(exception=e))
	    sys.exit(-1)


    @staticmethod
    def get_element_html(browser, params):
        """
        Get html code from web element
        """

        web_element = params[0]

        try:
            element = browser.find_element_by_xpath(web_element)
            html = element.get_attribute('outerHTML')
            if isinstance(html, unicode):
                return html.encode('utf-8')
            else:
                return html
        except Exception as e:
            logger.log('ERROR', 'Error getting html from {web_element}: {exception}'.format(web_element=web_element, exception=e))
            sys.exit(-1)


    @staticmethod
    def take_screenshot(browser, params):
        """
        Takes a screenshot of the browser
        """

        try:
            ss_path = params[0]
            ss_name = params[1]
        except LookupError:
            logger.log('ERROR', 'Function screenshot(): 2 arguments needed')
            sys.exit(-1)

        try:
            browser.save_screenshot('{ss_path}/{ss_name}.png'.format(ss_path=ss_path, ss_name=ss_name))
            logger.log('NOTE', 'Screenshot from {current_url} saved on: {ss_path}/{ss_name}.png'.format(current_url=browser.current_url, ss_path=ss_path, ss_name=ss_name))
        except Exception as e:
            logger.log('ERROR', 'Error taking screenshot: {exception}'.format(exception=e))
            sys.exit(-1)
