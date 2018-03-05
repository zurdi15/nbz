#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import lib_a_nb
import lib_b_nb
import lib_snf_nb
import lib_d_nb


# BOT FEATURES DICTIONARY

FEATURES_DICT = {

# Basic functions
'browser'           : '',
'get_url'           : lib_b_nb.get_url,
'fill'              : lib_b_nb.fill_field,
'clear'             : lib_b_nb.clear_field,
'click'             : lib_b_nb.click_element,
'select'            : lib_b_nb.select_option,
'wait'              : lib_b_nb.wait_time,
'back'              : lib_b_nb.back,
'forward'           : lib_b_nb.forward,
'refresh'           : lib_b_nb.refresh,
'get_text'          : lib_b_nb.get_text,
'current_url'       : lib_b_nb.current_url,

# Sniffering functions
'check_net'         : lib_snf_nb.check_net,
'export_net_report' : '',

# Advanced functions
'print'             : lib_a_nb.print_,
'random'	    : lib_a_nb.random,
'get_timestamp'	    : lib_a_nb.get_timestamp,
'timestamp_diff'    : lib_a_nb.timestamp_diff,
'open'		    : lib_a_nb.open_file,
'write'		    : lib_a_nb.write_file,
'write_table_as_csv': lib_a_nb.write_table_as_csv,
'close'		    : lib_a_nb.close_file,
'get_local_storage' : lib_a_nb.get_local_storage,
'set_local_storage' : lib_a_nb.set_local_storage,
'get_cookie'        : lib_a_nb.get_cookie,
'set_cookie'        : lib_a_nb.set_cookie,
'get_element'       : lib_a_nb.get_element,
'children_num'      : lib_a_nb.children_num,
'page_load_time'    : lib_a_nb.page_load_time,
'scroll_to_bottom'  : lib_a_nb.scroll_to_bottom,
'scroll_to_top'     : lib_a_nb.scroll_to_top,
'execute_js'        : lib_a_nb.execute_js,
'set_timeout'       : lib_a_nb.set_timeout,
'get_html'          : lib_a_nb.get_html,
'get_element_html'  : lib_a_nb.get_element_html,
'screenshot'        : lib_a_nb.take_screenshot,

# Data types functions
'int'		    : lib_d_nb.cast_int,
'float'		    : lib_d_nb.cast_float,
'str'		    : lib_d_nb.cast_str,
'sub_str'	    : lib_d_nb.sub_str,
'len'		    : lib_d_nb.lenght,
'find'		    : lib_d_nb.find,

}
