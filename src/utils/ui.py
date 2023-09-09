from .constants import CONST_COLOR_BLUE, CONST_COLOR_GREEN, CONST_COLOR_RED, CONST_COLOR_NORMAL, CONST_COLOR_YELLOW

def printb(text):
    """
    Prints the provided text in blue color.

    This function colors the terminal output text in blue. It relies on predefined 
    constant `CONST_COLOR_BLUE` which contains the necessary ANSI escape code for blue text.

    Parameters:
    - text (str): The text to be printed.

    Usage:
    ```python
    printb("This text will appear in blue!")
    ```

    """
    print(CONST_COLOR_BLUE + text)


def printg(text):
    """
    Prints the provided text in green color.

    This function colors the terminal output text in green. It relies on predefined 
    constant `CONST_COLOR_GREEN` which contains the necessary ANSI escape code for green text.

    Parameters:
    - text (str): The text to be printed.

    Usage:
    ```python
    printg("This text will appear in green!")
    ```

    """
    print(CONST_COLOR_GREEN + text)


def printr(text):
    """
    Prints the provided text in red color.

    This function colors the terminal output text in red. It relies on predefined 
    constant `CONST_COLOR_RED` which contains the necessary ANSI escape code for red text.

    Parameters:
    - text (str): The text to be printed.

    Usage:
    ```python
    printr("This text will appear in red!")
    ```

    """
    print(CONST_COLOR_RED + text)


def printn(text):
    """
    Prints the provided text in its normal color.

    This function returns the terminal output text to its default color using 
    the `CONST_COLOR_NORMAL` constant, which contains the necessary ANSI escape code 
    for resetting text color.

    Parameters:
    - text (str): The text to be printed.

    Usage:
    ```python
    printn("This text will appear in the default terminal color!")
    ```

    """
    print(CONST_COLOR_NORMAL + text)


def printy(text):
    """
    Prints the provided text in yellow color.

    This function colors the terminal output text in yellow. It relies on predefined 
    constant `CONST_COLOR_YELLOW` which contains the necessary ANSI escape code for yellow text.

    Parameters:
    - text (str): The text to be printed.

    Usage:
    ```python
    printy("This text will appear in yellow!")
    ```

    """
    print(CONST_COLOR_YELLOW + text)
