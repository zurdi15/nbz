#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
from lib_log_nbz import *
logger = Logging()


class LibSnf:


    def __init__(self):
        pass


    def check_net(self, har, request):
        if request[0] == 'params':
            return self.check_net_parameters(har, request)
        elif request[0] == 'keyword':
            return self.check_net_keywords(har, request)
        else:
            logger.log('ERROR', 'Not admited request type: ' + request[0])
            sys.exit(-1)
    
    
    def check_net_parameters(self, har, request):
        """
        Check if any request had choosen parameters
        Return selected value from any request
        """
    
        request_ok = False
        url = ''
        status_code = '404'
        timestamp = ''
        times = 0
    
        value = request[1] # Value to return
        params = request[2:] # Parsing just parameters to search
    
        for entry in har['log']['entries']:
            param_list_aux = entry['request']['url'].split('?')
            if len(param_list_aux) > 1:
                param_list = param_list_aux[1].split('&')
                if set(params).issubset(set(param_list)):
                    if value == 'times':
                        times += 1
                    else:
                        request_ok = True
                        status_code = int(entry['response']['status'])
                        url = entry['request']['url']
                        timestamp = entry['startedDateTime'].replace('T', ' ')[:-10]
                        break
    
        if value == 'request_ok':
            return request_ok
        elif value == 'url':
            return url
        elif value == 'status_code':
            return status_code
        elif value == 'timestamp':
            return timestamp
        elif value == 'times':
            return times
        else:
            logger.log('ERROR', 'Can\'t find ' + str(value) + ' - invalid search')
            sys.exit(-1)
    
    def check_net_keywords(self, har, request):
        """
        Check if any request had choosen url
        Return selected value from any request
        """
    
        request_ok = False
        url = ''
        status_code = 404
        timestamp = ''
    
        value = request[1] # Value to return
        keywords = request[2:] # Keywords to search
    
        for entry in har['log']['entries']:
            for keyword in keywords:
                if entry['request']['url'].find(keyword) != -1:
                    request_ok = True
                    status_code = int(entry['response']['status'])
                    url = entry['request']['url']
                    timestamp = entry['startedDateTime'].replace('T', ' ')[:-10]
                else:
                    request_ok = False
                    url = ''
                    status_code = 404
                    timestamp = ''
                    break
    
        if value == 'request_ok':
            return request_ok
        elif value == 'url':
            return url
        elif value == 'status_code':
            return status_code
        elif value == 'timestamp':
            return timestamp
        else:
            logger.log('ERROR', 'Can\'t find ' + str(value) + ' - invalid search')
            sys.exit(-1)
