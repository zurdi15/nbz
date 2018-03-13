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
except Exception:
    logger.log('ERROR', "Dependencies not installed. Please run install.sh")
    sys.exit(-1)
from user_agent import USER_AGENT_DICT


def start_proxy(proxy_path):
    """
    Start proxy to capture net traffic
    """

    logger.log('NOTE', 'Launching proxy server...')
    try:
        server = Server(proxy_path)
        server.start()
    except Exception as e:
        logger.log('ERROR', 'Error launching server: ' + str(e))
        sys.exit(-1)
    try:
        proxy = server.create_proxy()
    except Exception as e:
        logger.log('ERROR', 'Error configuring  proxy: ' + str(e))
        sys.exit(-1)
    return server, proxy


def instance_browser(proxy, params):
    """
    Start web browser
    """

    if len(params) < 1:
            logger.log('ERROR', 'Error launching browser')
            logger.log('ERROR', 'Browser incorrectly defined')
            sys.exit(-1)
    else:
        try:

            user_agent, user_agent_log = get_user_agent(params)
            logger.log('NOTE', 'Launching Browser: ' + str(params[0]) + ' (user-agent: ' + user_agent_log + ')')

            if params[0] == 'chrome':
                ch_opt = webdriver.ChromeOptions()
                proxy_url = urlparse.urlparse(proxy.proxy).path
                ch_opt.add_argument("--proxy-server=" + proxy_url)
                if user_agent != 'default':
                    ch_opt.add_argument("--user-agent=" + user_agent)
                browser = webdriver.Chrome(chrome_options=ch_opt)

            elif params[0] == 'firefox':
                ff_prf = webdriver.FirefoxProfile()
                if user_agent != 'default':
                    ff_prf.set_preference("general.useragent.override", user_agent)
                browser = webdriver.Firefox(firefox_profile=ff_prf, proxy=proxy.selenium_proxy())

            else:
                logger.log('ERROR', 'Not supported browser: ' + params[0])
                sys.exit(-1)

        except Exception as e:
            logger.log('ERROR', 'Error launching ' + str(params[0]) + '(' + str(params[1]) + '): ' + str(e))
            sys.exit(-1)
        return browser


def get_user_agent(params):
    """
    Return user_agent found in params, or default instead
    """

    if len(params) == 2:
        try:
            user_agent = USER_AGENT_DICT[params[1]]
            user_agent_log = params[1]
        except LookupError:
            logger.log('ERROR', 'Not supported user-agent: ' + str(params[1]))
            sys.exit(-1)
    else:
        user_agent = 'default'
        user_agent_log = 'default'

    return user_agent, user_agent_log
