#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import sys
import pickle
from lib_logger import *
logger = Logging()
try:
	import ply.yacc as yacc
except Exception:
	logger.log('ERROR', "Dependencies not installed. Please run install.sh.")
	sys.exit(-1)
from lexer_nb import tokens # Get the token map from the lexer
from features import FEATURES_DICT


def NBParser(instructions_path, interactive=False):

	# Dictionary of variables
	variables = {}

	# Dictionary of functions
	functions = FEATURES_DICT

	# z_code structure
	z_code = []


	# Initial state
	def p_sent_list(p):
		'''sent_list : sent_list sent
			     	 | sent
			     	 | empty'''
		if len(p) == 2:
			p[0] = [p[1]]
		else:
			p[0] = p[1]
			p[0].append(p[2])


	def p_sent(p):
		'''sent : sent_func_def
				| sent_assign
				| sent_func SEMI'''
		p[0] = p[1]
	
	
	# Functions definition
	def p_sent_funcs_def(p):
		'''sent_func_def : DEF ID LPAREN RPAREN LBRACE sent_list RBRACE'''
		functions[p[2]] = ''
		p[0] = ['def', p[2], p[6]]
		for sent in p[6]:
			z_code.pop()
		z_code.append(p[0])		


	# Assign definitions
	def p_sent_assign_expr(p):
		'''sent_assign : ID ASSIGN expr_type SEMI
					   | ID ASSIGN expr_arithm SEMI
					   | ID ASSIGN logic_list SEMI'''
		p[0] = ['assign', p[1], p[3]]
		variables[p[1]] = ''
		z_code.append(p[0])


        def p_sent_assign_func(p):
            '''sent_assign : ID ASSIGN sent_func SEMI'''
            z_code.pop()
	    p[0] = ['assign', p[1], p[3]]
	    variables[p[1]] = ''
	    z_code.append(p[0])

	
	# Function call expression
	def p_expr_funcs(p):
		'''sent_func : ID LPAREN list RPAREN'''
		try:
			check = functions[p[1]]
			p[0] = ['func', p[1], p[3]]
			z_code.append(p[0])
		except LookupError:
			logger.log('ERROR', 'Undefined function "' + str(p[1]) + '"  line ' + str(p.lineno(1)+1))
			sys.exit(-1)
	

	# List expressions
	def p_list_var(p):
		'''list : list COMMA ID
                | list COMMA sent_func
                | sent_func
                | ID'''
		if len(p) == 2:
			if isinstance(p[1], str):
				try:
					aux = variables[p[1]]
					p[0] = [['var', p[1]]]
				except LookupError:
					logger.log('ERROR', 'Undefined variable "' + str(p[1]) + '" line ' + str(p.lineno(1)+1))
					sys.exit(-1)
			elif isinstance(p[1], list):
				try:
					aux = functions[p[1][1]]
					p[0] = [p[1]]
					z_code.pop()
				except LookupError:
					logger.log('ERROR', 'Undefined function "' + str(p[1][1]) + '" line ' + str(p.lineno(1)+1))
					sys.exit(-1)
		else:
			p[0] = p[1]
			if isinstance(p[3], str):
				try:
					aux = variables[p[3]]
					p[0].append(['var', p[3]])
				except LookupError:
					logger.log('ERROR', 'Undefined variable "' + str(p[3]) + '" line ' + str(p.lineno(3)+1))
					sys.exit(-1)
			elif isinstance(p[3], list):
				try:
					aux = functions[p[3][1]]
					p[0].append([p[3]])
					z_code.pop()
				except LookupError:
					logger.log('ERROR', 'Undefined function "' + str(p[3][1]) + '" line ' + str(p.lineno(1)+1))
					sys.exit(-1)

	def p_list_value(p):
		'''list : list COMMA expr_type
				| expr_type
				| empty'''
		if len(p) == 2:
			p[0] = [['value', p[1]]]
		else:
			p[0] = p[1]
			p[0].append(['value', p[3]])


	def p_list_expression(p):
		'''list : list COMMA expr_arithm
				| list COMMA logic_list
				| expr_arithm
				| logic_list'''
		if len(p) == 2:
			p[0] = [p[1]]
		else:
			p[0] = p[1]
			p[0].append(p[3])
	
	
	# Flow control expressions
	
	# For	
	def p_sent_for_flow_int(p):
		'''sent : FOR LPAREN for_valid_expr COMMA for_valid_expr COMMA for_valid_iter RPAREN LBRACE sent_list RBRACE
				| FOR LPAREN ID IN ID RPAREN LBRACE sent_list RBRACE'''
		if len(p) == 10:
			p[0] = ['for', p[3], p[5], p[8]]
			variables[p[3]] = ''
			for i in xrange(0, len(p[8])):
				z_code.pop()
		else:
			p[0] = ['for', p[3], p[5], p[7], p[10]]
			for i in xrange(0, len(p[10])):
				z_code.pop()		
	        z_code.append(p[0])
	
	def p_for_valid_expressions_num(p):
		'''for_valid_expr : expr_num
				  		  | expr_arithm'''
		p[0] = p[1]


	def p_for_valid_iterators(p):
		'''for_valid_iter : PLUS
						  | PLUSPLUS
						  | MINUS
						  | MINUSMINUS'''
		p[0] = p[1]
	

	# If / else
	def p_sent_if_flow(p):
		'''sent : IF LPAREN logic_list RPAREN LBRACE sent_list RBRACE
				| IF LPAREN logic_list RPAREN LBRACE sent_list RBRACE elif_sent
				| IF LPAREN logic_list RPAREN LBRACE sent_list RBRACE ELSE LBRACE sent_list RBRACE
				| IF LPAREN logic_list RPAREN LBRACE sent_list RBRACE elif_sent ELSE LBRACE sent_list RBRACE'''
		if len(p) == 8: # Only if
			p[0] = ['if', p[3], p[6]]
			for i in xrange(0, len(p[6])):
				z_code.pop()
			z_code.append(p[0])

		elif len(p) == 9: # If + elif
			p[0] = ['if', p[3], p[6], p[8]]
			for i in xrange(0, len(p[6])):
				z_code.pop()
			z_code.append(p[0])

		elif len(p) == 12: # If + else
			p[0] = ['if', p[3], p[6], [['else']+[p[10]]]]
			for i in xrange(0, len(p[6])):
				z_code.pop()
			for i in xrange(0, len(p[10])):
				z_code.pop()
			z_code.append(p[0])

		elif len(p) == 13: # If + elif + else
			if not p[8]:
				p[0] = ['if', p[3], p[6], p[8], [['else']+[p[11]]]]
			else:
				p[0] = ['if', p[3], p[6], [['else']+[p[11]]]]
			for i in xrange(0, len(p[6])):
				z_code.pop()
			for i in xrange(0, len(p[11])):
				z_code.pop()
			z_code.append(p[0])

	# Elif 
	def p_sent_elif_flow(p):
		'''elif_sent : ELIF LPAREN logic_list RPAREN LBRACE sent_list RBRACE elif_sent
			     	 | empty'''
		if len(p) > 2:
			for i in xrange(0, len(p[6])):
				z_code.pop()
			if not p[8]:
				p[0] = [['elif', p[3], p[6]], p[8][0]]
			else:
				p[0] = [['elif', p[3], p[6]]]


	# While
	def p_sent_while_flow(p):
		'''sent : WHILE LPAREN logic_list RPAREN LBRACE sent_list RBRACE'''
		p[0] = ['while', p[3], p[6]]
		for i in xrange(0, len(p[6])):
			z_code.pop()
		z_code.append(p[0])
	
	
	# Logic list	
	def p_group_logic_list(p):
		'''logic_list : LPAREN logic_list RPAREN'''
		p[0] = p[2]
	
	
	def p_logic_list(p):
		'''logic_list : logic_list AND logic_list
					  | logic_list OR logic_list
					  | expr_bool'''
		if len(p) == 2:
			p[0] = p[1]
		else:
			if p[2] == 'and':
				p[0] = ['boolean', p[1], p[3], 'and']
			elif p[2] == 'or':
				p[0] = ['boolean', p[1], p[3], 'or']


	# Boolean expressions	
	def p_expr_logical(p):
		'''expr_bool : expr_bool EQ expr_bool
			     	 | expr_bool LT expr_bool
			     	 | expr_bool LET expr_bool
			     	 | expr_bool GT expr_bool
			     	 | expr_bool GET expr_bool
			     	 | expr_bool DIFF expr_bool
			     	 | NOT expr_bool'''
		if p[2] == '==':
			p[0] = ['boolean', p[1], p[3], '==']
		elif p[2] == '<':
			p[0] = ['boolean', p[1], p[3], '<']
		elif p[2] == '<=':
			p[0] = ['boolean', p[1], p[3], '<=']
		elif p[2] == '>':
			p[0] = ['boolean', p[1], p[3], '>']
		elif p[2] == '>=':
			p[0] = ['boolean', p[1], p[3], '=>']
		elif p[2] == '!=':
			p[0] = ['boolean', p[1], p[3], '!=']
		else:
			p[0] = ['boolean', p[1], p[1], 'not']

	
	def p_logic_valid_var(p):
		'''expr_bool : sent_func'''
		try:
		    aux = functions[p[1][1]]
		    z_code.pop()
		    p[0] = p[1]
		except LookupError:
		    logger.log('ERROR', 'Undefined function "' + str(p[1][1]) + '"  line ' + str(p.lineno(1)+1))
		    sys.exit(-1)

	
	def p_logic_valid_num(p):
		'''expr_bool : expr_num
			     	 | expr_arithm'''
		p[0] = p[1]
	

	# Arithmethic expressions
	def p_group_expr_arithmethic(p):
		'''expr_arithm : LPAREN expr_arithm RPAREN'''
		p[0] = p[2]


	def p_expr_aritmethic(p):
		'''expr_arithm : expr_arithm PLUS expr_arithm
					   | expr_arithm MINUS expr_arithm
					   | expr_arithm MULTIPLY expr_arithm
					   | expr_arithm DIVIDE expr_arithm
					   | MINUS expr_arithm'''
		if p[2] == '+':
			p[0] = ['arithm', p[1],  p[3], '+']
		elif p[2] == '-':
			p[0] = ['arithm', p[1],  p[3], '-']
		elif p[2] == '*':
			p[0] = ['arithm', p[1],  p[3], '*']
	 	elif p[2] == '/':
			p[0] = ['arithm', p[1],  p[3], '/']
		elif p[1] == '-':
			p[0] = ['arithm', p[2],  -1, '*']


	def p_arithm_valid_var(p):
		'''expr_arithm : ID
                       | sent_func'''
		if isinstance(p[1], str):
			try:
				aux = variables[p[1]]
				p[0] = ['var', p[1]]
			except LookupError:
				logger.log('ERROR', 'Undefined variable "' + str(p[1]) + '"  line ' + str(p.lineno(1)+1))
				sys.exit(-1)
		elif isinstance(p[1], list):
			try:
				aux = functions[p[1][1]]
				z_code.pop()
				p[0] = p[1]
			except LookupError:
				logger.log('ERROR', 'Undefined function "' + str(p[1][1]) + '"  line ' + str(p.lineno(1)+1))
				sys.exit(-1)


	def p_arithm_valid_num(p):
		'''expr_arithm : expr_type'''
		p[0] = p[1]
			

	# Type definitions
	def p_expr_type(p):
		'''expr_type : expr_num
			     	 | expr_string'''
		p[0] = p[1]	

	def p_expr_bool_true(p):
		'''expr_bool : TRUE'''
		p[0] = True


	def p_expr_bool_false(p):
		'''expr_bool : FALSE'''
		p[0] = False
	
	
	def p_expr_number(p):
		'''expr_num : FLOAT
			    	| INTEGER'''
		p[0] = p[1]
	
	
	def p_expr_string(p):
		'''expr_string : STRING'''
		p[0] = p[1]
	
	
	# Empty rule
	def p_empty(p):
		'''empty :'''
		p[0] = None
	
	
	# Error rule for syntax errors
	def p_error(p):
		if p is not None:
			logger.log('ERROR', 'Illegal token: "' + str(p.value) + '" at line: ' + str(p.lineno))
			sys.exit(-1)
		else:
			logger.log('ERROR', 'Unexpected end of input')

	
	# Build the parser
	parser = yacc.yacc(debug=1)
	
	
	if not interactive:
		z_code_path = instructions_path + 'code'
		z_code_path_vars = instructions_path + 'vars'
		data = ''
		with open(instructions_path, 'r') as f:
			for line in f:
				if len(line)>1:
					data += line
					if not line: continue
		try:
			parser.parse(data)
		except EOFError:
			logger.log('ERROR', 'General error parsing ' + instructions_path)
		with open(z_code_path, 'wb') as zcode:
			pickle.dump(z_code, zcode)
		with open(z_code_path_vars, 'wb') as zcode_vars:
			pickle.dump(variables, zcode_vars)
		return z_code, variables
	else:
		while True:
			s = raw_input('input(sentence) > ')
			if not s: continue
			result = parser.parse(s)
			print(result)


# Interactive mode
if __name__ == "__main__":
	NBParser('interactive', True)
