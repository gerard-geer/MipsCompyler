"""
File: reg.py
Author: Gerard Geer

This is a Register Registry to facilitate register coloring.
"""
class RegRegistry():

    __slots__ = ('regs')

    def __init__(self):

        # A dictionary from register names to usage count.
        self.regs = {'$t0':0,'$t1':0,'$t2':0,'$t3':0,'$t4':0,
                     '$t5':0,'$t6':0,'$t7':0,'$t8':0,'$t9':0,
                     '$s0':0,'$s1':0,'$s2':0,'$s3':0,'$s4':0,
                     '$s5':0,'$s6':0,'$s7':0}

    def takeReg(self, out):

        # Get a list of ('<reg>',<usage>) pairs.
        r = self.regs.items()

        # Sort them by usage.
        r.sort(key=lambda x: x[1])
        # Now we check to see if the least used one is actually free.
        if r[0][1] == 0:

            # Oh it looks like it is. Or was.
            self.regs[ r[0][0] ] += 1

            # Return the register name.
            return r[0][0]
            
        # Oh no! Looks like that register was already used.
        else:
            
            self.regs[ r[0][0] ] += 1

            # Emit some stack update instructions.
            # The potential for stack curruption is HUGE. Hopefully
            # the nature of tree traversal allows for stack-like requests.
            out.asm += 'sw '+r[0][0]+', 0($sp)\n'
            out.asm += 'addi $sp, $sp, -4\n'
            
            # Return the register name.
            return r[0][0]

    def returnReg(self, reg, out):
        
        # See if the register was pushed onto the stack.
        if self.regs[reg] > 1:

            # Oh it was? Crap. 
            out.asm += 'addi $sp, $sp, 4\n'
            out.asm += 'lw '+reg+', 0($sp)\n'

        # Update the usage count.
        self.regs[reg] -= 1