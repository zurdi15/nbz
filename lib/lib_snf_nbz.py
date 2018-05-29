#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import os
from pprint import pprint

BASE_DIR = '{base_dir}'.format(base_dir=os.path.dirname(os.path.realpath(__file__)))

from lib_log_nbz import *
logger = Logging()


class LibSnf:


    def __init__(self):
        self.sniffer_attr = {
            'request_ok'    : False,
            'url'           : '',
            'status_code'   : '404',
            'timestamp'     : '',
            'times'         : 0
        }


    def check_net(self, har, request):

        check_type = request[0]

        if check_type == 'params':
            return self.check_net_parameters(har, request)
        elif check_type == 'keyword':
            return self.check_net_keywords(har, request)
        else:
            logger.log('ERROR', 'Not admitted request type: {type}'.format(type=check_type))
            sys.exit(-1)
    
    
    def check_net_parameters(self, har, request):
        """
        Check if any request had chosen parameters
        Return selected value from any request
        """

        try:
            attribute = request[1] # Attribute to return
            params = request[2:] # Parsing just parameters to search
        except LookupError:
            logger.log('ERROR', 'Function check_net(): at least 3 argument needed')
            sys.exit(-1)

        for entry in har['log']['entries']:
            param_list_aux = entry['request']['url'].split('?')
            if len(param_list_aux) > 1:
                param_list = param_list_aux[1].split('&')
                if set(params).issubset(set(param_list)):
                    if attribute == 'times':
                        self.sniffer_attr['times'] += 1
                    else:
                        self.sniffer_attr['request_ok'] = True
                        self.sniffer_attr['status_code'] = int(entry['response']['status'])
                        self.sniffer_attr['url'] = entry['request']['url']
                        self.sniffer_attr['timestamp'] = entry['startedDateTime'].replace('T', ' ')[:-10]
                        break
        try:
            return self.sniffer_attr[attribute]
        except LookupError:
            logger.log('ERROR', 'Can\'t find {attribute} - invalid search'.format(attribute=attribute))
            sys.exit(-1)


    def check_net_keywords(self, har, request):
        """
        Check if any request had chosen url
        Return selected value from any request
        """

        attribute = request[1] # Attribute to return
        keyword = request[2] # Keywords to search

        for entry in har['log']['entries']:
            if entry['request']['url'].find(keyword) != -1:
                self.sniffer_attr['request_ok'] = True
                self.sniffer_attr['status_code'] = int(entry['response']['status'])
                self.sniffer_attr['url'] = entry['request']['url']
                self.sniffer_attr['timestamp'] = entry['startedDateTime'].replace('T', ' ')[:-10]
                break
        try:
            return self.sniffer_attr[attribute]
        except LookupError:
            logger.log('ERROR', 'Can\'t find {attribute} - invalid search'.format(attribute=attribute))
            sys.exit(-1)


    @staticmethod
    def net_report(params, script_name):
        """
        Create net report csv
        """

        file_name = params[0]

        net_reports_path = '{base_dir}/out/net_reports/{script_name}'.format(base_dir=BASE_DIR, script_name=script_name)
        complete_csv_path = '{net_reports_path}/complete_net_log_{report_name}.csv'.format(net_reports_path=net_reports_path, report_name=file_name)
        if not os.path.exists(net_reports_path):
            os.makedirs(net_reports_path)
        return open(complete_csv_path, 'w')


    @staticmethod
    def reset_har(set_net_report, complete_csv, current_url, proxy):
        """
        Reset proxy's HAR to check new requests
        """

        if set_net_report:
            complete_csv.write('URL: {url}\n\n'.format(url=current_url))
            pprint(proxy.har['log']['entries'], complete_csv)
        return proxy.new_har()