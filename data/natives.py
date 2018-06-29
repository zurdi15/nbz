#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import os
import sys

BASE_DIR = '{base_dir}'.format(base_dir=os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'lib'))


from lib_snf_nbz import LibSnf
lib_snf_nbz = LibSnf()
from lib_a_nbz import LibA
lib_a_nbz = LibA()
from lib_b_nbz import LibB
lib_b_nbz = LibB()
from lib_d_nbz import LibD
lib_d_nbz = LibD()


# BOT NATIVES

NATIVES = {

# System functions
'browser'           : '',
'exit'              : '',

# Basic functions
'get_url'           : lib_b_nbz.get_url,
'set_url_retries'   : lib_b_nbz.set_url_retries,
'fill'              : lib_b_nbz.fill_field,
'clear'             : lib_b_nbz.clear_field,
'click'             : lib_b_nbz.click_element,
'select'            : lib_b_nbz.select_option,
'wait'              : lib_b_nbz.wait_time,
'back'              : lib_b_nbz.back,
'forward'           : lib_b_nbz.forward,
'refresh'           : lib_b_nbz.refresh,
'get_text'          : lib_b_nbz.get_text,
'current_url'       : lib_b_nbz.current_url,

# Sniffing functions
'check_net'         : lib_snf_nbz.check_net,
'reset_har'         : lib_snf_nbz.reset_har,
'export_net_report' : lib_snf_nbz.net_report,

# Advanced functions
'print'             : lib_a_nbz.print_,
'random'            : lib_a_nbz.random,
'get_timestamp'     : lib_a_nbz.get_timestamp,
'timestamp_diff'    : lib_a_nbz.timestamp_diff,
'open'              : lib_a_nbz.open_file,
'write'             : lib_a_nbz.write_file,
'write_table_as_csv': lib_a_nbz.write_table_as_csv,
'close'             : lib_a_nbz.close_file,
'get_local_storage' : lib_a_nbz.get_local_storage,
'set_local_storage' : lib_a_nbz.set_local_storage,
'get_cookie'        : lib_a_nbz.get_cookie,
'set_cookie'        : lib_a_nbz.set_cookie,
'get_element'       : lib_a_nbz.get_element,
'children_num'      : lib_a_nbz.children_num,
'page_load_time'    : lib_a_nbz.page_load_time,
'scroll_down'       : lib_a_nbz.scroll_down,
'scroll_to_bottom'  : lib_a_nbz.scroll_to_bottom,
'scroll_up'         : lib_a_nbz.scroll_up,
'scroll_to_top'     : lib_a_nbz.scroll_to_top,
'execute_js'        : lib_a_nbz.execute_js,
'set_timeout'       : lib_a_nbz.set_timeout,
'export_html'       : lib_a_nbz.export_html,
'get_all_html_links': lib_a_nbz.get_all_html_links,
'get_element_html'  : lib_a_nbz.get_element_html,
'screenshot'        : lib_a_nbz.take_screenshot,

# Data types functions
'int'               : lib_d_nbz.cast_int,
'float'             : lib_d_nbz.cast_float,
'str'               : lib_d_nbz.cast_str,
'sub_str'           : lib_d_nbz.sub_str,
'len'               : lib_d_nbz.length,
'find'              : lib_d_nbz.find,
'replace'           : lib_d_nbz.replace,
'split'             : lib_d_nbz.split,
'append_list'       : lib_d_nbz.append_list,
'update_list'       : lib_d_nbz.update_list,
'remove_list'       : lib_d_nbz.remove_list,
'get_element_list'  : lib_d_nbz.get_element_list,

}
