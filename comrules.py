"""
File: comrules.py
Author: Gerard Geer

IMP has essentially three types of statements:
    Arithmetic
    Boolean
    Command

This file defines the parsing rules for commands, where
things get tricky.
"""
from comnodes import *

# Finally we have a quick rule for defining commands.
def p_command(t):
    '''
    command : succession
            | final
            | assignment
            | skip
            | ifthenelse
            | while
    '''
    t[0] = t[1]

# Succession. Oh jeez this one is the sticking point.
def p_succession(t):
    '''
    succession : command SEMI command
    '''
    t[0] = Succession(t[1],t[3])

# Final line. This is a new rule just to facilitate ending
# every line with semicolons.
def p_final(t):
    '''
    final : command SEMI
    '''
    t[0] = Succession(t[1],None)

# A quick rule for assignment.
def p_assignment(t):
    '''
    assignment : aexploc ASSIGN aexp
    '''
    t[0] = Assignment(t[1],t[3])

# A rule for the skip command.
def p_skip(t):
    '''
    skip : SKIP
    '''
    t[0] = Skip()

# The if statement rule.
def p_ifthenelse(t):
    '''
    ifthenelse : IF bexp THEN command ELSE command
    '''
    t[0] = IfThenElse(t[2], t[4], t[6])

# The while loop rule.
def p_while(t):
    '''
    while : WHILE bexp DO command
    '''
    t[0] = While(t[2], t[4])

