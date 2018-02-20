"""
File: aexpnodes.py
Author: Gerard Geer

This file defines all the Aexp node types for a compileable IMP AST.
"""
from nodes import CompileableASTNode

class AexpNum(CompileableASTNode):
        
    __slots__=('val')

    def __init__(self, val):
        self.val = val

    def comp(self, out, reg):
        # Just load an immediate into the register given to us.
        out.asm += 'li '+reg+', '+str(self.val)+'\n'

    def __str__(self):
        return 'AexpNum ('+str(self.val)+')'

    def getChildren(self):
        return None

class AexpLoc(CompileableASTNode):
        
    __slots__=('name')

    def __init__(self, name):
        self.name = name

    def comp(self, out, reg):
        # This one is pretty easy actually.
        out.asm += 'lw '+reg+', '+self.name+'\n'

    def __str__(self):
        return 'AexpLoc ('+self.name+')'

    def getChildren(self):
        return None

class AexpMult(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # Get registers for the operands.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)
        
        # Emit assembly for those constants, using the
        # registers we got for them.
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # Use those registers to emit a multiplication
        # and retrieval instruction
        out.asm += 'mult '+r1+', '+r2+'\n'
        out.asm += 'mflo '+reg+'\n'

        # Relenquish the registers since we're not using them
        # anymore.
        out.regs.returnReg(r2, out) # Do it in the right order OR ELSE.
        out.regs.returnReg(r1, out)

    def __str__(self):
        return 'AexpMult'

    def getChildren(self):
        return (self.l, self.r)

class AexpAdd(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # Get registers for the operands.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)
        
        # Emit assembly for those constants, using the
        # registers we got for them.
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # Use those registers to emit a multiplication
        # and retrieval instruction
        out.asm += 'add '+reg+', '+r1+', '+r2+'\n'

        # Relenquish the registers since we're not using them
        # anymore.
        out.regs.returnReg(r2, out) # Do it in the right order OR ELSE.
        out.regs.returnReg(r1, out)

    def __str__(self):
        return 'AexpAdd'

    def getChildren(self):
        return (self.l, self.r)

class AexpSub(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # Get registers for the operands.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)
        
        # Emit assembly for those constants, using the
        # registers we got for them.
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # Use those registers to emit a multiplication
        # and retrieval instruction
        out.asm += 'sub '+reg+', '+r1+', '+r2+'\n'

        # Relenquish the registers since we're not using them
        # anymore.
        out.regs.returnReg(r2, out) # Do it in the right order OR ELSE.
        out.regs.returnReg(r1, out)

    def __str__(self):
        return 'AexpSub'

    def getChildren(self):
        return (self.l, self.r)
