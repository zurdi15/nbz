#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import re
from lib.lib_log_nbz import Logging

logger = Logging()


class LibD:
    """Data types library of native functions.

    This class contains all the data types functions to handle types into nbz-scripts.

    Methods:
        cast_int
        cast_float
        cast_str
        sub_str
        length
        find
        find_regex
        replace
        split
        append_list
        update_list
        remove_list
        get_element_list
    """

    def __init__(self):
        """Init LibD class"""

        pass

    @staticmethod
    def cast_int(browser, params):
        """Cast numeric string | float value to integer

        Args:
            browser: web browser instance
            params: list of parameters
                -0: value to convert to string (string | float)
        Returns:
            Integer of the converted data
        """

        value = params[0]
        try:
            return int(value)
        except Exception as e:
            raise Exception('Error casting {value} to integer: {exception}'.format(value=value,
                                                                                   exception=e))

    @staticmethod
    def cast_float(browser, params):
        """Cast numeric string | integer value to float

        Args:
            browser: web browser instance
            params: list of parameters
                -0: value to convert to float (integer | string)
        Returns:
            Float of the converted data
        """

        value = params[0]
        try:
            return float(value)
        except Exception as e:
            raise Exception('Error casting {value} to float: {exception}'.format(value=value,
                                                                                 exception=e))

    @staticmethod
    def cast_str(browser, params):
        """Cast numeric value to string

        Args:
            browser: web browser instance
            params: list of parameters
                -0: value to convert to string (integer | float)
        Returns:
            String of the converted number
        """

        value = params[0]
        try:
            return str(value)
        except Exception as e:
            raise Exception('Error casting {value} to str: {exception}'.format(value=value,
                                                                               exception=e))

    @staticmethod
    def sub_str(browser, params):
        """Returns substring from bigger string

        Args:
            browser: web browser instance
            params: list of parameters
                -0: string from extracting
                -1: start character index of substring (to the end if -2 is empty)
                -2: end character index of substring (optional)
        Returns:
            Substring from main string
        """

        try:
            string = params[0]
            substring_index_start = params[1]
        except LookupError:
            raise Exception('Function sub_str(): at least 2 arguments needed')

        try:
            if len(params) == 2:
                return string[substring_index_start:]
            else:
                substring_index_end = params[2]
                return string[substring_index_start:substring_index_end]
        except Exception as e:
            raise Exception('Error getting substring from {string}: {exception}'.format(string=string,
                                                                                        exception=e))

    @staticmethod
    def length(browser, params):
        """Returns length from any compatible data (string, list, dict)

        Args:
            browser: web browser instance
            params: list of parameters
                -0: data which can be measured (string, list, dict)
        Returns:
            Integer number of the length of the data
        """

        data = params[0]
        try:
            return len(data)
        except Exception as e:
            raise Exception('Error getting length from {data}: {exception}'.format(data=data,
                                                                                   exception=e))

    @staticmethod
    def find(browser, params):
        """Search one string into another string.

        Args:
            browser: web browser instance
            params: list of parameters
                -0: main string
                -1: substring to search
        Returns:
            -1 if substring is not found
            Integer of the character index where the substring starts on the main string
        """

        try:
            string = params[0]
            substring = params[1]
        except LookupError:
            raise Exception('Function find(): 2 arguments needed')

        try:
            return string.find(substring)
        except Exception as e:
            raise Exception('Error searching substring into {string}: {exception}'.format(string=string,
                                                                                          exception=e))

    @staticmethod
    def find_regex(browser, params):
        """Search a regex pattern into string.

        Args:
            browser: web browser instance
            params: list of parameters
                -0: main string
                -1: regex
        Returns:
            String found with that pattern
        """

        try:
            string = params[0]
            pattern = params[1]
            result = re.search(pattern, string)
            if result:
                return result.group()
            else:
                return ""
        except Exception as e:
            raise Exception('Error searching pattern into {pattern}: {exception}'.format(pattern=pattern,
                                                                                        exception=e))

    @staticmethod
    def replace(browser, params):
        """Replace substring into string

        Args:
            browser: web browser instance
            params: list of parameters
                -0: main string
                -1: old substring to replace
                -2: new substring to put
        Returns:
            String with the new substring replaced on old substring
        """

        try:
            string = params[0]
            substring_old = params[1]
            substring_new = params[2]
        except LookupError:
            raise Exception('Function replace(): 3 arguments needed')

        try:
            return string.replace(substring_old, substring_new)
        except Exception as e:
            raise Exception('Error replacing: {string}({old}, {new}): {exception}'.format(string=string,
                                                                                          old=substring_old,
                                                                                          new=substring_new,
                                                                                          exception=e))

    @staticmethod
    def split(browser, params):
        """Split string into some strings with a delimiter

        Args:
            browser: web browser instance
            params: list of parameters
                -0: string to split
                -1: delimiter to split with
        Returns:
            A list of substrings from main string between delimiters
        """

        try:
            string = params[0]
            delimiter = params[1]
        except LookupError:
            raise Exception('Function split(): 2 arguments needed')

        try:
            return string.split(delimiter)
        except Exception as e:
            raise Exception('Error splitting: {string} with {delimiter}: {exception}'.format(string=string,
                                                                                             delimiter=delimiter,
                                                                                             exception=e))

    @staticmethod
    def append_list(browser, params):
        """Append an element into a list

        Args:
            browser: web browser instance
            params: list of parameters
                -0: list
                -1: element to append
        Returns:
            List with the new element at the end
        """

        try:
            list_ = params[0]
            element = params[1]
        except LookupError:
            raise Exception('Function append(): 2 arguments needed')

        try:
            return list_.append(element)
        except Exception as e:
            raise Exception('Error appending {element} into {list}: {exception}'.format(element=element,
                                                                                        list=list_,
                                                                                        exception=e))

    @staticmethod
    def update_list(browser, params):
        """Update an element on a list

        Args:
            browser: web browser instance
            params: list of parameters
                -0: list
                -1: index of the element to upadte
                -2: new element
        Returns:
            A list with the new element updated
        """

        try:
            list_ = params[0]
            index = params[1]
            element = params[2]
        except LookupError:
            raise Exception('Function update(): 3 arguments needed')

        try:
            list_[index] = element
            return list_
        except Exception as e:
            raise Exception('Error updating {index} into {list} with {element}: {exception}'.format(index=index,
                                                                                                    list=list_,
                                                                                                    element=element,
                                                                                                    exception=e))

    @staticmethod
    def remove_list(browser, params):
        """Remove and element from a list

        Args:
            browser: web browser instance
            params: list of parameters
                -0: list
                -1: element to remove
        Returns:
            A list with the element removed
        """

        try:
            list_ = params[0]
            element = params[1]
        except LookupError:
            raise Exception('Function remove(): 2 arguments needed')

        try:
            return list_.remove(element)
        except Exception as e:
            raise Exception('Error removing {element} from {list}: {exception}'.format(element=element,
                                                                                       list=list_,
                                                                                       exception=e))

    @staticmethod
    def get_element_list(browser, params):
        """Return element from list with index

        Args:
            browser: web browser instance
            params: list of parameters
                -0: list
                -1: index of the wanted element
        Returns:
            Element of the list
        """

        try:
            list_ = params[0]
            index = params[1]
        except LookupError:
            raise Exception('Function get_element_list(): 2 arguments needed')

        try:
            return list_[index]
        except Exception as e:
            raise Exception('Error getting element {index} from list {list}: {exception}'.format(index=index,
                                                                                                 list=list_,
                                                                                                 exception=e))
