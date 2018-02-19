"""
File: aexprules.py
Author: Gerard Geer

IMP has essentially three types of statements:
    Arithmetic
    Boolean
    Command

This file defines the parsing rules for Arithmetic expressions,
also known as Aexps.
"""
from aexpnodes import *

# A general rule for Aexps. Note that evaluation of locations and
# numbers are evaluated in separate rules to avoid post-lex lexing.
# It would be nice if they disjoint union'd these tokens with some
# stuff like types.
def p_aexp(t):
    '''
    aexp : aexpplus
         | aexpminus
         | aexpmult
         | aexpnum
         | aexploc
    '''
    t[0] = t[1]

# A quick breakout rule for addition.
def p_aexpplus(t):
    '''
    aexpplus : aexp PLUS aexp
    '''
    t[0] = AexpAdd(t[1],t[3])

# A quick breakout rule for addition.
def p_aexpminus(t):
    '''
    aexpminus : aexp MINUS aexp
    '''
    t[0] = AexpSub(t[1],t[3])

# A quick breakout rule for addition.
def p_aexpmult(t):
    '''
    aexpmult : aexp MULT aexp
    '''
    t[0] = AexpMult(t[1],t[3])

# A rule for Aexps that simply evaluates numbers.
# This allows us to not need to check the type of unary exps.
def p_aexpnum(t):
    '''
    aexpnum : NUM
    '''
    t[0] = AexpNum(int(t[1]))

# A rule for Aexps that are just locations. Like the prior
# rule, this is for simplifying the general Aexp rule.
def p_aexploc(t):
    '''
    aexploc : LOC
    '''
    t[0] = AexpLoc(t[1])
