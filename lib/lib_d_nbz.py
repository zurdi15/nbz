#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
from lib_log_nbz import Logging
logger = Logging()


class LibD:


    def __init__(self):
        pass


    @staticmethod
    def cast_int(browser, params):
        """
        Cast numeric string | float value to integer
        """

        value = params[0]

        try:
            return int(value)
        except Exception as e:
            logger.log('ERROR', 'Error casting {value} to integer: {exception}'.format(value=value, exception=e))
            sys.exit(-1)


    @staticmethod
    def cast_float(browser, params):
        """
        Cast numeric string | integer value to float
        """

        value = params[0]

        try:
            return float(value)
        except Exception as e:
            logger.log('ERROR', 'Error casting {value} to float: {exception}'.format(value=value, exception=e))
            sys.exit(-1)


    @staticmethod
    def cast_str(browser, params):
        """
        Cast numeric value to string
        """

        value = params[0]

        try:
            return str(value)
        except Exception as e:
            logger.log('ERROR', 'Error casting {value} to str: {exception}'.format(value=value, exception=e))
            sys.exit(-1)


    @staticmethod
    def sub_str(browser, params):
        """
        Returns substring from bigger string
        """

        try:
            string = params[0]
            substring_index_start = params[1]
        except LookupError:
            logger.log('ERROR', 'Function sub_str(): at least 2 arguments needed')
            sys.exit(-1)

        try:
            if len(params) == 2:
                return string[substring_index_start:]
            else:
                substring_index_end = params[2]
                return string[substring_index_start:substring_index_end]
        except Exception as e:
            logger.log('ERROR', 'Error getting substring from {string}: {exception}'.format(string=string, exception=e))
            sys.exit(-1)


    @staticmethod
    def length(browser, params):
        """
        Returns length from any compatible data
        """

        data = params[0]

        try:
            return len(data)
        except Exception as e:
            logger.log('ERROR', 'Error getting length from {data}: {exception}'.format(data=data, exception=e))
            sys.exit(-1)


    @staticmethod
    def find(browser, params):
        """
        Search one string into another string
        If it is found, returns starting position of the string searched
        If don't, returns -1
        """

        try:
            string = params[0]
            substring = params[1]
        except LookupError:
            logger.log('ERROR', 'Function find(): 2 arguments needed')
            sys.exit(-1)

        try:
            return string.find(substring)
        except Exception as e:
            logger.log('ERROR', 'Error searching substring into {string}: {exception}'.format(string=string, exception=e))
            sys.exit(-1)


    @staticmethod
    def replace(browser, params):
        """
        Replace substring into string
        """

        try:
            string = params[0]
            substring_old = params[1]
            substring_new = params[2]
        except LookupError:
            logger.log('ERROR', 'Function replace(): 3 arguments needed')
            sys.exit(-1)

        try:
            return string.replace(substring_old, substring_new)
        except Exception as e:
            logger.log('ERROR', 'Error replacing: {string}({old}, {new}): {exception}'.format(string=string, old=substring_old, new=substring_new, exception=e))
            sys.exit(-1)


    @staticmethod
    def split(browser, params):
        """
        Split string into some strings with a delimiter
        """

        try:
            string = params[0]
            delimiter = params[1]
        except LookupError:
            logger.log('ERROR', 'Function split(): 2 arguments needed')
            sys.exit(-1)

        try:
            return string.split(delimiter)
        except Exception as e:
            logger.log('ERROR', 'Error splitting: {string} with {delimiter}: {exception}'.format(string=string, delimiter=delimiter, exception=e))
            sys.exit(-1)


    @staticmethod
    def append_list(browser, params):
        """
        Append an element into a list
        """

        try:
            list_ = params[0]
            element = params[1]
        except LookupError:
            logger.log('ERROR', 'Function append(): 2 arguments needed')
            sys.exit(-1)

        try:
            return list_.append(element)
        except Exception as e:
            logger.log('ERROR', 'Error appending {element} into {list}: {exception}'.format(element=element, list=list_, exception=e))
            sys.exit(-1)


    @staticmethod
    def update_list(browser, params):
        """
        Update an element on a list
        """

        try:
            list_ = params[0]
            index = params[1]
            element = params[2]
        except LookupError:
            logger.log('ERROR', 'Function update(): 3 arguments needed')
            sys.exit(-1)

        try:
            list_[index] = element
            return list_
        except Exception as e:
            logger.log('ERROR', 'Error updating {index} into {list} with {element}: {exception}'.format(index=index, list=list_, element=element, exception=e))
            sys.exit(-1)


    @staticmethod
    def remove_list(browser, params):
        """
        Remove and element from a list
        """

        try:
            list_ = params[0]
            element = params[1]
        except LookupError:
            logger.log('ERROR', 'Function remove(): 2 arguments needed')
            sys.exit(-1)

        try:
            return list_.remove(element)
        except Exception as e:
            logger.log('ERROR', 'Error removing {element} from {list}: {exception}'.format(element=element, list=list_, exception=e))
            sys.exit(-1)


    @staticmethod
    def get_element_list(browser, params):
        """
        Return element from list with index
        """

        try:
            list_ = params[0]
            index = params[1]
        except LookupError:
            logger.log('ERROR', 'Function get_element_list(): 2 arguments needed')
            sys.exit(-1)

        try:
            return list_[index]
        except Exception as e:
            logger.log('ERROR', 'Error getting element {index} from list {list}: {exception}'.format(index=index, list=list_, exception=e))
            sys.exit(-1)
