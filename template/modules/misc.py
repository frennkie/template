# -*- coding: utf-8 -*-
#
# Name:         misc.py
# Description:  Misc
#
# Author:       mail@rhab.de
# Date:         1970-01-01

### Versioning
__version_info__ = ('0', '1', 'dev2')
__version__ = '.'.join(__version_info__)

### Imports
import requests
import unittest2

### Functions

def say_hello():
    print "Hello World"

### not really needed:
def main():
    say_hello()

if __name__ == "__main__":
    main()

#EOF
