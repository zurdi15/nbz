#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import os
import argparse
from pprint import pprint
from pyvirtualdisplay import Display

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

if os.name == 'posix':
    proxy_path = os.path.join(BASE_DIR, 'proxy', 'bin', 'browsermob-proxy')
elif os.name == 'nt':
    proxy_path = os.path.join(BASE_DIR, 'proxy', 'bin', 'browsermob-proxy.bat')

sys.path.append(os.path.join(BASE_DIR, 'lib'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'parser'))

from nbz_core import NBZCore
from nbz_parser import NBZParser
from natives import NATIVES
from lib_log_nbz import Logging
logger = Logging()


class NBZInterface:
    """Interface between all modules of the nbz.

    This class provides all the attributes needed to the core module, using the parser module
    to parse the nbz-script previously. After all script is done, this class ends all connections.

    Attributes:
        coreAttributes: dictionary of attributes needed for the core module
        nbzCore: instance of the core module
    """


    def __init__(self, script, debug):
        """Inits NBZInterface class with some attributes"""

        self.core_attributes = {
            'instruction_set'   : '',
            'variables'         : {},
            'NATIVES'           : NATIVES,
            'USER_FUNC'         : {},

            'script'            : script,
            'script_name'       : os.path.basename(script)[0:-4],
            'debug'             : debug,

            # Proxy binaries to execute the sniffer
            'proxy_path'        : proxy_path,

            # Flag to instance browser once (even if z_code has more than one instance)
            'set_browser'       : False,
            'server'            : None,
            'proxy'             : None,
            'browser'           : None,

            'set_net_report'    : False,
            'net_reports_path'  : '',
            'complete_csv_path' : '',
            'complete_csv'      : None,
        }

        self.compile_script()
        nbz_core = NBZCore(self.core_attributes)
        nbz_core.execute_instructions()

        # Return all core attributes to close needed
        self.core_attributes = NBZCore.get_attributes(nbz_core)

        # Close browser/proxy/server
        if self.core_attributes['set_browser']:
            self.close_all()


    def compile_script(self):
        """Compile script to be executed.

        Returns:
            A lists structure with all the nbz-script converted
            A dict mapping variables of the script and their values
        """

        try:
            z_code, z_code_vars = NBZParser(self.core_attributes['script'])
            self.core_attributes['instruction_set'] = z_code
            self.core_attributes['variables'] = z_code_vars
            if self.core_attributes['debug']:
                logger.log('NOTE', 'Instructions: {instructions}'.format(instructions=self.core_attributes['instruction_set']))
                logger.log('NOTE', 'Variables: {variables}'.format(variables=self.core_attributes['variables']))
        except Exception as e:
            logger.log('ERROR', 'Script not compiled ({script}): {exception}'.format(script=self.core_attributes['script'], exception=e))
            sys.exit(-1)


    def close_all(self):
        """Close all connections and export har log"""

        if self.core_attributes['set_net_report']:
            self.core_attributes['complete_csv'].write('URL: {url}\n\n'.format(url=self.core_attributes['browser'].current_url))
            pprint(self.core_attributes['proxy'].har['log']['entries'], self.core_attributes['complete_csv'])
            self.core_attributes['complete_csv'].close()
            logger.log('NOTE', 'Complete_net csv file exported to: {net_report_csv}'.format(net_report_csv=self.core_attributes['complete_csv'].name))
        self.core_attributes['browser'].close()
        self.core_attributes['proxy'].close()
        self.core_attributes['server'].stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-script", help="script file", required=True)
    parser.add_argument("-debug", help="debug mode", required=False)
    parser.add_argument("-display", help="enable display emulation", required=False)
    args = parser.parse_args()
    script = args.script
    debug = args.debug
    display = args.display
    if debug == 'True':
        debug = True
    if display == 'True':
        display = Display(visible=0, size=(1024, 768))
        display.start()
    NBZInterface(script, debug)


if __name__ == "__main__":
    sys.exit(main())
