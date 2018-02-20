"""
File: aexpnodes.py
Author: Gerard Geer

This file defines all the command node types for a compileable IMP AST.
"""
from nodes import CompileableASTNode

class Succession(CompileableASTNode):

    __slots__=('first','second')

    def __init__(self, first, second):
        self.first = first
        self.second = second
    
    def comp(self, out, reg):
        print 'first line: '+str(type(self.first))
        print 'second line: '+str(type(self.second))
        r = out.regs.takeReg(out)
        if self.first != None:
            self.first.comp(out,r)
        if self.second != None:
            self.second.comp(out,r)
        out.regs.returnReg(r,out)
    
    def __str__(self):
        return 'Succession'

    def getChildren(self):
        return (self.first, self.second)


class Assignment(CompileableASTNode):

    __slots__=('loc','aexp')

    def __init__(self, loc, aexp):
        self.loc = loc
        self.aexp = aexp

    def comp(self, out, reg):

        out.asm += '\n# Assignment\n'
        # We actually don't need to use the register passed in.

        # First let's check to see if we need to create the var or
        # update it.
        if not self.loc.name in out.vars:
            out.data += self.loc.name + ': .word 0\n'
            out.vars.add(self.loc.name)

        # Now we need to emit code to compute the value of the aexp.
        #r = out.regs.takeReg(out)
        self.aexp.comp(out,reg)

        # Now that we have that value in r, we can emit code to store it.
        out.asm += 'sw '+reg+', '+self.loc.name+'\n'

        # Free r.
        #out.regs.returnReg(r, out)
    
    def __str__(self):
        return 'Assignment'

    def getChildren(self):
        return (self.loc, self.aexp)

class Skip(CompileableASTNode):

    __slots__=()

    def comp(self, out, reg):
        out.asm += 'nop\n'
    
    def __str__(self):
        return 'Skip'

    def getChildren(self):
        return None

class IfThenElse(CompileableASTNode):

    __slots__ = ('test','t','f')

    def __init__(self, test, t, f):
        self.test = test
        self.t = t
        self.f = f

    def comp(self, out, reg):

        out.asm += '\n# IfThenElse\n'
        
        # Generate labels for the various places we'll need to jump around.
        name = hex(id(self))
        false_tag = 'false_'+name
        exit_tag = 'exit_'+name

        # Okay first we need a register to store the result of the test.
        r = out.regs.takeReg(out)
        
        # Now let's emit code to do the test.
        out.asm += '\n# Test section\n'
        self.test.comp(out,r)

        # Now we need to emit code to branch to the false section.
        name = hex(id(self))
        false_tag = 'false_'+name
        exit_tag = 'exit_'+name
        out.asm += 'beq '+r+', $zero, '+false_tag+'\n'

        # At this point we can emit code to do the true section.
        out.asm += '\n# True section\n'
        self.t.comp(out,reg)

        # We don't want to flow into the false section, so...
        out.asm += 'j '+exit_tag+'\n'

        # And now the false section.
        out.asm += '\n# False section\n'
        out.asm += false_tag+':\n'
        self.f.comp(out,reg)

        out.asm += '\n# If Then Else exit\n'
        out.asm += '\n'+exit_tag+':\n'

        # Return the test's register to the register gods.
        out.regs.returnReg(r, out)
    
    def __str__(self):
        return 'IfThenElse'

    def getChildren(self):
        return (self.test, self.t, self.f)

class While(CompileableASTNode):

    __slots__ = ('test', 'command')

    def __init__(self, test, command):
        self.test = test
        self.command = command

    def comp(self, out, reg):

        out.asm += '\n# While\n'

        # Okay first we need to come up with section tags.
        name = hex(id(self))
        test_tag = 'test_'+name
        exit_tag = 'exit_'+name

        # Now let's generate the test section.
        r = out.regs.takeReg(out)
        
        out.asm += '# Loop test section\n'
        out.asm += test_tag+':\n'
        self.test.comp(out,r)

        # Now we need to create the branching statement.
        out.asm += 'beq '+r+', $zero, '+exit_tag+'\n'

        # Now we can create the body.
        out.asm += '\n# Loop body section\n'
        self.command.comp(out,reg)

        # Oh dangit we need another jump back to the test.
        out.asm += 'j '+test_tag+'\n'

        # And now we can emit a blank tag to jump to to exit the loop.
        out.asm += '\n# Loop exit\n'
        out.asm += exit_tag+':\n'

        # Return the test's register to the register gods.
        out.regs.returnReg(r, out)
    
    def __str__(self):
        return 'While'

    def getChildren(self):
        return (self.test, self.command)

