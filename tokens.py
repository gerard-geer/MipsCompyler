"""
File: tokens.py
Author: Gerard Geer

Defines token names and regexes for the IMP language.
"""


# Token name definitions.
tokens = ('NUM','LOC',
          'PLUS','MINUS','MULT',
          'TRUE','FALSE',
          'EQU','LEQ','NOT','AND','OR',
          'SKIP','SEMI','ASSIGN',
          'IF','THEN','ELSE','WHILE','DO')

# Token rule definitions.
t_TRUE      = r'true'
t_FALSE     = r'false'
t_NUM       = r'[-]?[0-9]*\.?[0-9]+'
t_LOC       = r'[A-Z]+[A-Za-z0-9]*'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULT      = r'\*'
t_SKIP      = r'skip'
t_SEMI      = r';'
t_ASSIGN    = r':='
t_EQU       = r'=='
t_LEQ       = r'<='
t_NOT       = r'!'
t_AND       = r'\&\&'
t_OR        = r'\|\|'
t_IF        = r'if'
t_THEN      = r'then'
t_ELSE      = r'else'
t_WHILE     = r'while'
t_DO        = r'do'

# Ignore spaces, tabs and newlines.
t_ignore = " \t\n"

# Create a rule for when errors are encountered.
def t_error(t):
    print("Bad token: '%s'" % t)
    t.lexer.skip(1)
