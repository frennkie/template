# -*- coding: utf-8 -*-
#
# Name:         misc.py
# Description:  Misc
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)

# Imports

# Functions


def say_hello_world():
    """Return the string "Hello World".

    This function returns the static string "Hello World".
    It is only a demo.

    Args:
        None

    Returns:
        str: "Hello World"

    Examples:
        This is complete doctest for this function.

        >>> print(say_hello_world())
        Hello World

    """
    return "Hello World"

def say_hello(name):
    """Return the string "Hello " and the passed name.

    This function returns the static string "Hello World".
    It is only a demo.

    Args:
        name (str): Name
            Pass a name "Bob" in order to get "Hello Bob".
            Again, just a demo.

    Returns:
        str: "Hello " + name

    Examples:
        Here are three Doctest examples for usage of this function.

        >>> print(say_hello("Bob"))
        Hello Bob

        >>> print(say_hello("Alice Cooper"))
        Hello Alice Cooper

        >>> print(say_hello("New Line"))
        Hello New Line

    """
    return "Hello " + name

def main():
    pass

if __name__ == "__main__":
    main()

# EOF
