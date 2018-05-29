#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>

import sys
import urlparse
from lib_log_nbz import *
logger = Logging()
try:
    from selenium import webdriver
    from browsermobproxy import Server
except LookupError:
    logger.log('ERROR', "Dependencies not installed. Please run install.sh")
    sys.exit(-1)
from user_agents import USER_AGENTS


class LibWb:


    def __init__(self):
        pass
    

    @staticmethod
    def instance_browser(proxy_path, params):
        """
        Start web browser
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
            try:
                user_agent = USER_AGENTS[params[1]]
            except LookupError:
                user_agent = params[1]
        except LookupError:
            logger.log('ERROR', 'Function browser(): 2 arguments needed')
            sys.exit(-1)

        try:
            logger.log('NOTE', 'Launching Browser: {engine} (user-agent: {user_agent})'.format(engine=engine, user_agent=user_agent))

            if engine == 'chrome':
                ch_opt = webdriver.ChromeOptions()
                proxy_url = urlparse.urlparse(proxy.proxy).path
                ch_opt.add_argument("--proxy-server=" + proxy_url)
                if user_agent != 'default':
                    ch_opt.add_argument("--user-agent=" + user_agent)
                try:
                    browser = webdriver.Chrome(chrome_options=ch_opt)
                except LookupError:
                    time.sleep(5)
                    browser = webdriver.Chrome(chrome_options=ch_opt)

            elif engine == 'firefox':
                ff_prf = webdriver.FirefoxProfile()
                if user_agent != 'default':
                    ff_prf.set_preference("general.useragent.override", user_agent)
                browser = webdriver.Firefox(firefox_profile=ff_prf, proxy=proxy.selenium_proxy())

            else:
                logger.log('ERROR', 'Not supported browser: {engine}'.format(engine=engine))
                sys.exit(-1)

        except Exception as e:
            logger.log('ERROR', 'Error launching {engine} ({user_agent}): {exception}'.format(engine=engine, user_agent=user_agent, exception=e))
            sys.exit(-1)
        return server, proxy, browser