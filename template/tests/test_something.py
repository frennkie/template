# -*- coding: utf-8 -*-
#
# Name:         test_something.py
# Description:  Test Something
#
# Author:       mail@rhab.de
# Date:         1970-01-01

### Versioning
__version_info__ = ('0', '1', 'dev2')
__version__ = '.'.join(__version_info__)

### Imports
import unittest2 as unittest


class TestSomething(unittest.TestCase):

    def test_function1_fake(self):
        print "This is fake! (Something)"
        self.assertEqual(True, True)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

#EOF
