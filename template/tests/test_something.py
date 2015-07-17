# -*- coding: utf-8 -*-
#
# Name:         test_something.py
# Description:  Test Something
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
__version_info__ = ('0', '4', '0')
__version__ = '.'.join(__version_info__)

# make sure (early) to add parent dir (main app) to path
import os.path
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, os.pardir))

# Imports
import unittest2 as unittest
import something


class TestSomething(unittest.TestCase):

    def test_fake1(self):
        self.assertEqual(True, something.fake())


def main():
    unittest.main()

if __name__ == "__main__":
    main()

# EOF
