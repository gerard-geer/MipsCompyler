#!/usr/bin/python
"""
File: imp.py
Author: Gerard Geer
Takes the first parameter passed to this program, considers it a filename,
assumes its an IMP file, and then tries to compile it.
"""

from sys import argv
import ply.lex as lex
import ply.yacc as yacc
from mcc import Output

# This is the top level rule.
def p_exp(t):
    '''
    exp : command
        | bexp
        | aexp
    '''
    t[0] = t[1]

# Import all the other rules.
from tokens import *
from bexprules import *
from aexprules import *
from comrules import *

# Finally the syntax error rule.
def p_error(t):
    print("Syntax error at '%s'" % t.type)

"""
The main function of this exercise. Tidies things up a bit.
"""
def main():

    # Do basic parameter checking.
    if len(argv) > 3:
        print 'Usage:'
        print './imp.py <infile>'
        print './imp.py <infile> <outfile>'
        return
    
    # Create the lexer.
    lexer = lex.lex()
    # Build the parser.
    parser = yacc.yacc()


    # Open the file and dump it into a string.
    f = open(argv[1])
    s = ''
    for line in f:
        s += line
    f.close()

    # Print the file contents.
    print 'Start of source code'
    print '===================='
    print s
    print '=================='
    print 'End of source file'

    # Do the compilation.
    ast = parser.parse(s)
    out = Output(ast)
    src = out.generateSource()

    if len(argv) == 2:
        print '\n\nStart of generated assembly'
        print '==========================='
        print src
        print '========================='
        print 'End of generated assembly'
    else:
        f = open(argv[2],'w')
        f.write(src)
    
    out.printAST()

    
            
if __name__ == "__main__":
    main()