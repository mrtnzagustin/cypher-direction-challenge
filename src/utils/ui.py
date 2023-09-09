from .constants import CONST_COLOR_BLUE, CONST_COLOR_GREEN, CONST_COLOR_RED, CONST_COLOR_NORMAL, CONST_COLOR_YELLOW

def printb(text):
    """Print text in blue"""
    print(CONST_COLOR_BLUE + text)

def printg(text):
    """Print text in green"""
    print(CONST_COLOR_GREEN + text)
    
def printr(text):
    """Print text in red"""
    print(CONST_COLOR_RED + text)

def printn(text):
    """Print text in normal color"""
    print(CONST_COLOR_NORMAL + text)
    
def printy(text):
    """Print text in yellow"""
    print(CONST_COLOR_YELLOW + text)