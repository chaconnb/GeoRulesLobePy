
# Code Better Practices
Reminders on how to make my code more organized and legible for others. Read : https://numpydoc.readthedocs.io/en/latest/example.html

### Functions:
- Avoid building long functions.
- Functions are constructed whenever there is a local variable that won't be used later in the code.
- Function names should be lowercase, with words separated by underscores as necessary to improve readability.

### Docstrings: 
An example is worth a thousand words: (see https://numpydoc.readthedocs.io/en/latest/example.html)

```
    Summarize the function in one line.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    *args : iterable
        Other arguments.
    long_var_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.
    type_without_description

    Other Parameters
    ----------------
    only_seldom_used_keyword : int, optional
        Infrequently used parameters can be described under this optional
        section to prevent cluttering the Parameters section.
    **kwargs : dict
        Other infrequently used keyword arguments. Note that all keyword
        arguments appearing after the first parameter specified under the
        Other Parameters section, should also be described under this
        section.

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    numpy.array : Relationship (optional).
    numpy.ndarray : Relationship (optional), which could be fairly long, in
                    which case the line wraps here.
    numpy.dot, numpy.linalg.norm, numpy.eye

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a Greek symbol like :math:`\omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a = [1, 2, 3]
    >>> print([x + 3 for x in a])
    """
    """
    [4, 5, 6]
    >>> print("a\nb")
    a
    b
    """
```

### Variable names:

### Line lenghts: 
Limit all lines to a maximum of 79 characters.
### Classes: 
class Square: 
    
    def __init__(self, lenght, width):
        self.length = length
        self.width = width
        self.area = lenght * width

    
from dataclass import dataclass



square = Square(3, 4)
bob = Square(3,4)
square.area 

def get_area(length, width): 
    return length * width

def get_special_area(shape,u):
    """get area from a Square instancec."""
    return shape.area + u

def get_area(shape:Square): 
    l = shape.lenght 
    w = shape.width 
    area = l * w 
    return area

get_special_area(bob,9)

