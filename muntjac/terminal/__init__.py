"""Provides classes and interfaces that wrap the terminal-side functionalities
for the server-side application.
"""

def clsname(cls):
    """@return: fully qualified name of given class"""
    return cls.__module__ + "." + cls.__name__


def fullname(obj):
    """@return fully qualified name of given object's class"""
    return clsname(obj.__class__)
