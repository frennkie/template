# -*- coding: utf-8 -*-
#
# Name:         test_misc.py
# Description:  Test Misc
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
# __version_info__ = ('0', '1', 'dev2')
# __version__ = '.'.join(__version_info__)

# make sure (early) that parent dir (main app) is in path
import os.path
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, os.pardir))

# Imports
import unittest2 as unittest
import modules.misc as misc


class TestMisc(unittest.TestCase):

    def test_say_hello_ok(self):
        self.assertEqual("Hello World", misc.say_hello())


def main():
    unittest.main()

if __name__ == "__main__":
    main()

# EOF
