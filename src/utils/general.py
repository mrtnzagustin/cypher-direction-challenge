from .constants import CONST_EMPTY_STRING

def is_defined(variable):
    """Returns true if the variable is defined, false otherwise"""
    return variable != CONST_EMPTY_STRING and variable != None