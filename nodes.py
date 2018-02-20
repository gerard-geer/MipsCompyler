"""
file: nodes.py
Author: Gerard Geer

This is the prototypical class for an compileable AST node. Man, Python's
inheritance functionality is strange.
"""
from abc import ABCMeta, abstractmethod

class CompileableASTNode(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def comp(self, out, reg):
        pass
    @abstractmethod
    def __str__(self):
        pass
    @abstractmethod
    def getChildren(self):
        pass