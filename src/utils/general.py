from .constants import CONST_EMPTY_STRING

def is_defined(variable):
    """
    Determines if a variable is defined based on its value.

    This function checks whether the given variable is neither an empty string 
    (as represented by `CONST_EMPTY_STRING`) nor a `None` value. Essentially, 
    it is used to determine if a variable has been meaningfully defined or assigned 
    a value.

    Parameters:
    - variable (Any): The variable whose definition status is to be checked. 
      Can be of any data type.

    Returns:
    - bool: 
        - `True` if the variable is defined (not an empty string and not `None`).
        - `False` otherwise.

    Usage:
    ```python
    name = "John"
    is_name_defined = is_defined(name)  # Returns True
    ```

    Note:
    - For the sake of this function, 'defined' means the variable holds a value 
      other than an empty string or `None`. It doesn't actually check if a variable 
      exists in the local or global namespace.

    """
    return variable != CONST_EMPTY_STRING and variable != None