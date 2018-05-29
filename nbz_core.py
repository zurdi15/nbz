#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

from lib_wb_nbz import LibWb
lib_wb_nbz = LibWb()
from lib_log_nbz import Logging
logger = Logging()


class NBZCore:


    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['USER_FUNC'] = {}
        self.execute_instructions(self.attributes['instruction_set'])


    def get_attributes(self):
        return self.attributes


    def execute_instructions(self, instruction_set):
        """
        Execute each instruction from instruction_set (recursively on flow control sentences)
        instruction[0] -> type:
            - assign:       instruction[1] -> id
                            instruction[2] -> value | expression
            - def
                            instruction[1] -> id
                            instruction[2] -> block of sentences

            - func:         instruction[1] -> id
                            instruction[2] -> parameters list

            - if:	        instruction[1] -> condition
                            instruction[2] -> block of sentences (if)
                            instruction[3] -> block of sentences (else)

            - for(normal):  instruction[1] -> start index
                            instruction[2] -> end index
                            instruction[3] -> mode (+ | ++ | - | --)
                            instruction[4] -> block of sentences

            - for(foreach): instruction[1] -> iterable variable
                            instruction[2] -> list
                            instruction[3] -> block of sentences

            - while:	    instruction[1] -> condition
                            instruction[2] -> block of sentences
        """

        def get_value(sub_instruction):
            """
            Local function to get direct value or variable value of a parameter
            Local function to resolve arithmetic expressions
            Local function to resolve boolean expressions
            Local function to resolve function return value
            """

            if isinstance(sub_instruction, list):
                if len(sub_instruction) > 0:
                    if sub_instruction[0] == 'var':
                        return self.attributes['variables'][sub_instruction[1]]
                    elif sub_instruction[0] == 'value':
                        return sub_instruction[1]
                    elif sub_instruction[0] == 'arithm':
                        if sub_instruction[3] == '+':
                            try:
                                    op_1 = get_value(sub_instruction[1]).encode('utf-8')
                            except TypeError:
                                    op_1 = get_value(sub_instruction[1])
                            try:
                                    op_2 = get_value(sub_instruction[2]).encode('utf-8')
                            except TypeError:
                                    op_2 = get_value(sub_instruction[2])
                            if isinstance(op_1, str) or isinstance(op_2, str):
                                    return str(op_1) + str(op_2)
                            else:
                                    return op_1 + op_2
                        else:
                            return eval(str(get_value(sub_instruction[1])) + sub_instruction[3] + str(get_value(sub_instruction[2])))
                    elif sub_instruction[0] == 'boolean':
                        if sub_instruction[3] != 'not':
                            op_1 = get_value(sub_instruction[1])
                            op_2 = get_value(sub_instruction[2])
                            if isinstance(op_1, str):
                                op_1 = "'{op_1}'".format(op_1=op_1)
                            if isinstance(op_2, str):
                                op_2 = "'{op_2}'".format(op_2=op_2)
                            return eval(str(op_1) + ' ' + sub_instruction[3] + ' ' + str(get_value(op_2)))
                        else:
                            return not get_value(sub_instruction[1])
                    elif sub_instruction[0] == 'func':
                        sub_params = []
                        for sub_param in sub_instruction[2]:
                            sub_params.append(get_value(sub_param))
                        if sub_instruction[1] == 'check_net':
                            return self.attributes['NATIVES']['check_net'](self.attributes['proxy'].har, params)
                        else:
                            return self.attributes['NATIVES'][sub_instruction[1]](self.attributes['browser'], params)
                    else:
                        return sub_instruction
                else:
                    return sub_instruction
            else:
                return sub_instruction

        # Main execution loop
        for instruction in instruction_set:
            try:
                if instruction[0] == 'assign':
                    self.attributes['variables'][instruction[1]] = get_value(instruction[2])
                elif instruction[0] == 'def':
                    self.attributes['USER_FUNC'][instruction[1]] = instruction[2]
                elif instruction[0] == 'func':
                    params = []
                    for param in instruction[2]:
                        params.append(get_value(param))
                    if instruction[1] == 'exit':
                        sys.exit(0)
                    elif instruction[1] == 'browser':
                        if not self.attributes['set_browser']:
                            try:
                                self.attributes['server'], self.attributes['proxy'], self.attributes['browser'] = lib_wb_nbz.instance_browser(self.attributes['proxy_path'], params)
                            except Exception as e:
                                print str(e)
                                sys.exit(-1)
                            self.attributes['set_browser'] = True
                        else:
                            logger.log('ERROR', 'Browser already instanced')
                    elif instruction[1] == 'export_net_report':
                        self.attributes['complete_csv'] = self.attributes['NATIVES']['net_report'](params, self.attributes['script_name'])
                        self.attributes['set_net_report'] = True
                    elif instruction[1] == 'reset_har':
                        self.attributes['NATIVES']['reset_hat'](self.attributes['set_ner_report'], self.attributes['complete_csv'], self.attributes['browser'].current_url, self.attributes['proxy'])
                    elif instruction[1] == 'check_net':
                        pass
                    else:
                        try:
                            self.attributes['NATIVES'][instruction[1]](self.attributes['browser'], params)
                        except LookupError:
                            try:
                                self.execute_instructions(self.attributes['USER_FUNC'][instruction[1]])
                            except LookupError:
                                logger.log('ERROR', 'Not defined function')
                                sys.exit(-1)
                elif instruction[0] == 'if':
                    if get_value(instruction[1]):
                        self.execute_instructions(instruction[2])
                    else:
                        if len(instruction) == 4: # If statement have elif OR else
                            if instruction[3][0][0] == 'elif':
                                for elif_ in instruction[3]:
                                    if get_value(elif_[1]):
                                        self.execute_instructions(elif_[2])
                                        break
                            elif instruction[3][0][0] == 'else':
                                self.execute_instructions(instruction[3][0][1])
                        elif len(instruction) == 5: # If statement have elif AND else
                            elif_done = False
                            for elif_ in instruction[3]:
                                if get_value(elif_[1]):
                                    elif_done = True
                                    self.execute_instructions(elif_[2])
                                    break
                            if not elif_done:
                                self.execute_instructions(instruction[4][0][1])
                elif instruction[0] == 'for':
                    if len(instruction) == 4: # Foreach
                        element = get_value(instruction[1])
                        structure = self.attributes['variables'][get_value(instruction[2])]
                        for aux_element in structure:
                            if isinstance(structure, file):
                                self.attributes['variables'][element] = aux_element[0:-1] # Avoiding newline character if we loop for a file lines
                            else:
                                self.attributes['variables'][element] = aux_element # All other structure types
                            self.execute_instructions(instruction[3])
                    else: # Standard For
                        if instruction[3] == '+':
                            for i in xrange(get_value(instruction[1]), get_value(instruction[2]), 1):
                                self.execute_instructions(instruction[4])
                        elif instruction[3] == '++':
                            for i in xrange(get_value(instruction[1]), get_value(instruction[2]), 2):
                                self.execute_instructions(instruction[4])
                        elif instruction[3] == '-':
                            for i in xrange(get_value(instruction[1]), get_value(instruction[2]), -1):
                                self.execute_instructions(instruction[4])
                        elif instruction[3] == '--':
                            for i in xrange(get_value(instruction[1]), get_value(instruction[2]), -2):
                                self.execute_instructions(instruction[4])
                elif instruction[0] == 'while':
                    while get_value(instruction[1]):
                        self.execute_instructions(instruction[2])
            except Exception as e:
                logger.log('ERROR', 'Error executing instruction {type}: {exception}'.format(type=instruction[0], exception=e))
                sys.exit(-1)