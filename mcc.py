"""
File: line.py
Author: Gerard Geer

Encapsulates a line with its AST, variables and constants.
"""
from reg import RegRegistry

class Output():

    __slots__ = ('asm','ast','vars','refs', 'regs')

    def __init__(self, ast):
        self.asm = ''
        self.data = ''
        self.ast = ast
        self.vars = set()
        self.regs = RegRegistry()

    def _printASTHelper(self, ast, level):

        print '| '*level + str(ast)

        children = ast.getChildren()
        if children == None:
            return 

        for child in children:
            if child != None: # Argh inner conditionals
                self._printASTHelper(child, level+1)

    def printAST(self):
        self._printASTHelper(self.ast, 0)

    def _compile(self):

        # Get a starting register in case the top level instruction needs one.
        r = self.regs.takeReg(self)

        # Start off the cascading compilation.
        self.ast.comp(self,r)

        # Return that original register.
        self.regs.returnReg(r,self)
        
    def generateSource(self):

        # Kick off compilation.
        self._compile()

        # A nice little header comment.
        src = '#'+ '='*79 +  \
            "\n# Generated with Gerard's MIPS compiler.\n" +    \
              '#'+ '='*79 + '\n\n'

        # Start off with the data section.
        src += '.data\n'
        src += self.data

        # Add in the text section.
        src += '\n.text\n'
        src += self.asm

        # Don't forget to actually leave the program.
        src += '\n# exit.\nli $v0 10\nsyscall\n'

        # Close it all off with a footer.
        src += '#'+ '='*79 +  \
             "\n# END OF FILE.\n" +    \
               '#'+ '='*79 + '\n'
        
        return src