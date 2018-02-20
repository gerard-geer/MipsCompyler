"""
File: bexpnodes.py
Author: Gerard Geer

This is another Node definition module, this time for boolean expression nodes.
"""
from nodes import CompileableASTNode

class BexpTrue(CompileableASTNode):
        
    __slots__=()

    def comp(self, out, reg):
        # Having it be MAX_INT speeds some things up.
        out.asm += 'li '+reg+', 0xFFFFFFFF\n'

    def __str__(self):
        return 'BexpTrue'

    def getChildren(self):
        return None

class BexpFalse(CompileableASTNode):
        
    __slots__=()

    def comp(self, out, reg):
        # False, on the other hand, is 0 like always.
        out.asm += 'li '+reg+', 0x00000000\n'

    def __str__(self):
        return 'BexpFalse'

    def getChildren(self):
        return None

class BexpNot(CompileableASTNode):
    
    __slots__=('r')

    def __init__(self,r):
        self.r = r

    def comp(self, out, reg):
        
        # First we need to declare a register to put the results of the
        # right hand side of the NOT operation into, so we can not them
        # into the register we ourselves were given.
        r1 = out.regs.takeReg(out)

        # Compile the right hand side.
        self.r.comp(out,r1)

        # This is why True is 0xFFFFFFFF.
        out.asm += 'not '+reg+', '+r1+'\n'

        # Return our dinnerware to the buttery.
        out.regs.returnReg(r1)

    def __str__(self):
        return 'BexpFalse'

    def getChildren(self):
        return (self.r)

class BexpEqu(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # Again, get registers for the operands.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)

        # Now we need to add code for the operands.
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # Now that we have results for the operands, we can
        # go ahead and add this node's code to the output.
        out.asm += 'sne '+reg+', '+r1+', '+r2+'\n'

        # Now we have 0 on true and 1 on false,
        #  but we need to get to 0xFFFFFFFF on true, and 0x0 on false.
        # This is a slow down in equality testing for speedups elsewhere,
        # but adders in MIPS machines are always of the exotic variety.
        out.asm += 'sub '+reg+', '+reg+', 1\n'

        # Return the registers for great good.
        out.regs.returnReg(r2, out)
        out.regs.returnReg(r1, out)
    
    def __str__(self):
        return 'BexpEqu'

    def getChildren(self):
        return (self.l, self.r)

class BexpLeq(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # This pattern is well established at this point.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # Hey how about that? We need 0 on true and 1 on false, and it just
        # so happens that greater than is the perfectly disjoint complement
        # of LEQ.
        out.asm += 'sgt '+reg+', '+r1+', '+r2+'\n'

        # Do the same habberdashery to get 0xFFFFFFFF and 0x0
        out.asm += 'sub '+reg+', '+reg+', 1\n'

        # Return the registers for great good.
        out.regs.returnReg(r2, out)
        out.regs.returnReg(r1, out)
    
    def __str__(self):
        return 'BexpLeq'

    def getChildren(self):
        return (self.l, self.r)

class BexpAnd(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # This pattern is well established at this point.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # By setting true to 0xFFFFFFFF, we can use a really fast
        # bitwise AND to do this comparison.
        out.asm += 'and '+reg+', '+r1+', '+r2+'\n'

        # Return the registers for great good.
        out.regs.returnReg(r2, out)
        out.regs.returnReg(r1, out)
    
    def __str__(self):
        return 'BexpAnd'

    def getChildren(self):
        return (self.l, self.r)

class BexpOr(CompileableASTNode):

    __slots__=('l','r')

    def __init__(self, l,r):
        self.l = l
        self.r = r

    def comp(self, out, reg):

        # This pattern is well established at this point.
        r1 = out.regs.takeReg(out)
        r2 = out.regs.takeReg(out)
        self.l.comp(out,r1)
        self.r.comp(out,r2)

        # By setting true to 0xFFFFFFFF, we can use a really fast
        # bitwise OR too!
        out.asm += 'or '+reg+', '+r1+', '+r2+'\n'

        # Return the registers for great good.
        out.regs.returnReg(r2, out)
        out.regs.returnReg(r1, out)
    
    def __str__(self):
        return 'BexpOr'

    def getChildren(self):
        return (self.l, self.r)