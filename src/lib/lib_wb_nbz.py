#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import platform
import time
from urllib.parse import urlparse
from data.user_agents import USER_AGENTS
from lib.lib_log_nbz import Logging
from selenium import webdriver
from browsermobproxy import Server
logger = Logging()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
proxy_path = os.path.join(BASE_DIR, '..', '..', 'proxy', 'bin', 'browsermob-proxy')


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

    def instance_browser(self, proxy_enabled, params):
        """Start web browser and proxy server

        Args:
            proxy_enabled: flag to set proxy
            params: list of parameters
                -0: browser engine
                -1: user-agent
        Returns:
            Instance of the server, the proxy and the web browser
        """

        if proxy_enabled:
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
                proxy_url = urlparse.urlparse(proxy.proxy).path
            except AttributeError:
                proxy_url = urlparse(proxy.proxy).path
        else:
            server = None
            proxy = None
        try:
            engine = params[0]
            try:
                user_agent = USER_AGENTS[params[1]]
            except LookupError:
                user_agent = params[1]
            headless = params[2]
        except LookupError:
            raise Exception('Function browser(): 3 arguments needed')
        try:
            logger.log('NOTE', 'Engine: {engine} | User-agent: {user_agent} | Headless: {headless}'.format(engine=engine,
                                                                                                           user_agent=user_agent,
                                                                                                           headless=headless))
            if engine == 'chrome':
                driver_path = self.get_driver_path(engine)
                ch_opt = webdriver.ChromeOptions()
                if proxy_enabled:
                    ch_opt.add_argument("--proxy-server=" + proxy_url)
                if user_agent != 'default':
                    ch_opt.add_argument("--user-agent=" + user_agent)
                if headless:
                    ch_opt.headless = True
                try:
                    browser = webdriver.Chrome(executable_path=driver_path,
                                               chrome_options=ch_opt)
                except LookupError:
                    time.sleep(5)
                    browser = webdriver.Chrome(executable_path=driver_path,
                                               chrome_options=ch_opt)
            elif engine == 'firefox':
                driver_path = self.get_driver_path(engine)
                ff_prf = webdriver.FirefoxProfile()
                ff_opt = webdriver.FirefoxOptions()
                if user_agent != 'default':
                    ff_prf.set_preference("general.useragent.override", user_agent)
                if headless:
                    ff_opt.headless = True
                try:
                    browser = webdriver.Firefox(executable_path=driver_path, firefox_profile=ff_prf, proxy=proxy.selenium_proxy(), options=ff_opt) if proxy_enabled \
                    else webdriver.Firefox(executable_path=driver_path, firefox_profile=ff_prf, options=ff_opt)
                except LookupError:
                    time.sleep(5)
                    browser = webdriver.Firefox(executable_path=driver_path, firefox_profile=ff_prf, proxy=proxy.selenium_proxy(), options=ff_opt) if proxy_enabled \
                    else webdriver.Firefox(executable_path=driver_path, firefox_profile=ff_prf, options=ff_opt)
            else:
                raise Exception('Not supported engine: {engine}'.format(engine=engine))
        except Exception as e:
            raise Exception('Error launching {engine} ({user_agent}): {exception}'.format(engine=engine,
                                                                                          user_agent=user_agent,
                                                                                          exception=e))
        return browser

    @staticmethod
    def get_driver_path(engine):
        """Method to get the driver path for each engine and each operative system

        Args:
            engine: web browser to execute the nbz-script
        Returns:
            The driver path of the selected engine
        """

        if engine == 'chrome':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver')
        elif engine == 'firefox':
                driver_path = os.path.join(BASE_DIR, 'drivers', 'geckodriver')
        else:
            raise Exception('Not supported engine {engine}'.format(engine=engine))
        return driver_path
