#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: <Zurdi>


import ply.lex as lex


# -- Reserved words token list --
reserved = {

    # Flow control
    'if'        :'IF',
    'elif'      :'ELIF',
    'else'      :'ELSE',
    'for'       :'FOR',
    'in'        :'IN',
    'while'     :'WHILE',

    # Logical operators
    'true'      :'TRUE',
    'false'     :'FALSE',
    'or'        :'OR',
    'and'       :'AND',
    'not'       :'NOT',

    # Statements
    'def'       :'DEF',

}

# --- TOKENS LIST ---
tokens = [

    # Types
    'FLOAT',
    'INTEGER',
    'STRING',

    # Aritmethic operators
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'PLUSPLUS',
    'MINUSMINUS',

    # Logical operators
    'EQ',
    'LT',
    'LET',
    'GT',
    'GET',
    'DIFF',

    # Lexical tokens
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'SEMI',
    'COLON',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'ID',

] + list(reserved.values())


# --- REGULAR EXPRESSION RULES FOR TOKENS ---

# Types
def t_FLOAT(t):
    r'\d+[\.]\d*'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t): # Trimming strings rule (avoiding " in the string token)
    r'\'([^\']|(\\\'))*\''
    t.value = str(t.value)[1:-1]
    return t


# Arithmetic operators
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_MULTIPLY      = r'\*'
t_DIVIDE        = r'/'
t_PLUSPLUS      = r'\+\+'
t_MINUSMINUS    = r'--'

# Logical operators
t_EQ            = r'=='
t_LT            = r'<'
t_GT            = r'>'
t_LET           = r'<='
t_GET           = r'>='
t_DIFF          = r'!='

# Lexical tokens
t_ASSIGN        = r'='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_COMMA         = r'\,'
t_SEMI          = r'\;'
t_COLON         = r'\:'
t_LBRACE        = r'\{'
t_RBRACE        = r'\}'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'


def t_ID(t):
    r'[a-z_A-Z]([a-z_A-Z0-9])*'
    t.type = reserved.get(t.value.lower(),'ID') # Check for reserved words (lower() to avoid case-sensitive)
    return t


# --- MISC ---

# - Ignored characters

# Spaces and tabs
t_ignore = ' \t'


# Comments
def t_comment(t):
    r'\#.*'


# Newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    raise Exception("Illegal character '" + t.value[0] + "' line: " + str(t.lineno) + " column: " + str(t.lexpos))


# Build the lexer
lexer = lex.lex()


# Interactive mode
if __name__ == "__main__":
    lexer = lex.lex()
    while True:
        lex.input(raw_input('input(token) > '))
        tok = lex.token()
        print tok
