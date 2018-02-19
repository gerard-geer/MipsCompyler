"""
File: bexprules.py
Author: Gerard Geer

IMP has essentially three types of statements:
    Arithmetic
    Boolean
    Command

This file defines the parsing rules for Boolean expressions,
also known as Bexps.
"""
from bexpnodes import *

# This rule defines boolean expressions, or Bexps.
# I'm not sure why we can't test the equvalence of
# two Bexps though.
def p_bexp(t):
    '''
    bexp : bexptrue
         | bexpfalse
         | bexpequ
         | bexpleq
         | bexpnot
         | bexpand
         | bexpor
    '''
    t[0] = t[1]

# A rule for breaking out not.
def p_bexpnot(t):
    '''
    bexpnot : NOT bexp
    '''
    t[0] = BexpNot(t[1])

# Equality.
def p_bexpequ(t):
    '''
    bexpequ : aexp EQU aexp
    '''
    t[0] = BexpEqu(t[1],t[3])

# Less-than-or-equal
def p_bexpleq(t):
    '''
    bexpleq : aexp LEQ aexp
    '''
    t[0] = BexpLeq(t[1],t[3])

# bexp AND bexp.
def p_bexpand(t):
    '''
    bexpand : bexp AND bexp
    '''
    t[0] = BexpAnd(t[1],t[3])

# bexp OR bexp.
def p_bexpor(t):
    '''
    bexpor : bexp OR bexp
    '''
    t[0] = BexpOr(t[1],t[3])

# A breakout rule for truth.
def p_bexptrue(t):
    '''
    bexptrue : TRUE
    '''
    t[0] = BexpTrue()

# A breakout rule for false.
def p_bexpfalse(t):
    '''
    bexpfalse : FALSE
    '''
    t[0] = BexpTrue()
