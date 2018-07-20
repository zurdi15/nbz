#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import sys
import time
import urlparse

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

from lib_log_nbz import Logging
logger = Logging()
try:
    from selenium import webdriver
    from browsermobproxy import Server
except LookupError:
    logger.log('ERROR', "Dependencies not installed. Please run install.sh")
    sys.exit(-1)
from user_agents import USER_AGENTS


class LibWb:
    """Browser and proxy library.

    This class contains the methods to start the proxy and the native function to start the web browser.
    """


    def __init__(self):
        """Inits LibWb class"""

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

        logger.log('NOTE', 'Launching proxy server...')
        try:
            server = Server(proxy_path)
            server.start()
        except Exception as e:
            logger.log('ERROR', 'Error launching server: {exception}'.format(exception=e))
            sys.exit(-1)
        try:
            proxy = server.create_proxy()
        except LookupError:
            time.sleep(5)
            try:
                proxy = server.create_proxy()
            except Exception as e:
                logger.log('ERROR', 'Error configuring  proxy: {exception}'.format(exception=e))
                sys.exit(-1)
        proxy.new_har()

        try:
            engine = params[0]
            driver_path = self.get_driver_path(engine)
            try:
                user_agent = USER_AGENTS[params[1]]
            except LookupError:
                user_agent = params[1]
        except LookupError:
            logger.log('ERROR', 'Function browser(): 2 arguments needed')
            sys.exit(-1)

        try:
            logger.log('NOTE', 'Launching Browser: {engine} (user-agent: {user_agent})'.format(engine=engine,
                                                                                               user_agent=user_agent))

            if engine == 'chrome':
                ch_opt = webdriver.ChromeOptions()
                proxy_url = urlparse.urlparse(proxy.proxy).path
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
            elif engine == 'phantom':
                browser = webdriver.PhantomJS(driver_path)
            else:
                logger.log('ERROR', 'Not supported browser: {engine}'.format(engine=engine))
                sys.exit(-1)

        except Exception as e:
            logger.log('ERROR', 'Error launching {engine} ({user_agent}): {exception}'.format(engine=engine,
                                                                                              user_agent=user_agent,
                                                                                              exception=e))
            sys.exit(-1)
        return server, proxy, browser


    @staticmethod
    def get_driver_path(engine):
        """Method to get the driver path for each engine and each operative system

        Args:
            engine: web browser to execute the nbz-script
        Returns:
            The driver pathj of the selected engine
        """

        if engine == 'chrome':
            if os.name == 'posix':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver')
            elif os.name == 'nt':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver.exe')
            else:
                logger.log('ERROR', 'Operative System not supported')
                sys.exit(-1)
        elif engine == 'firefox':
            if os.name == 'posix':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'geckodriver')
            elif os.name == 'nt':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'geckodriver.exe')
            else:
                logger.log('ERROR', 'Operative System not supported')
                sys.exit(-1)
        elif engine == 'phantom':
            if os.name == 'posix':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'phantomjs')
            elif os.name == 'nt':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'phantomjs.exe')
            else:
                logger.log('ERROR', 'Operative System not supported')
                sys.exit(-1)
        else:
            driver_path = ''
        return driver_path

