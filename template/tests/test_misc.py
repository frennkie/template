# -*- coding: utf-8 -*-
#
# Name:         test_misc.py
# Description:  Test Misc
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
__version_info__ = ('0', '6', '2')
__version__ = '.'.join(__version_info__)

# make sure (early) that parent dir (main app) is in path
import os.path
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, os.pardir))

# Imports
import unittest2 as unittest
import mock
import subprocess

import modules.misc as misc


class TestMisc(unittest.TestCase):

    def test_say_hello_ok(self):
        self.assertEqual("Hello World", misc.say_hello_world())


    # Generic SubProcess Tester
    # https://gist.github.com/wingyplus/5555656
    class MockPopen(object):
        def __init__(self):
            pass
        def communicate(self, input=None):
            pass
        @property
        def returncode(self):
            pass

    def test_rsync_remote_to_local_with_mock_subprocess_successful(self):
        mock_popen = TestMisc.MockPopen()
        mock_popen.communicate = mock.Mock(return_value=('hello mock subprocess stdout', 'hello mock subprocess stderr'))
        mock_returncode = mock.PropertyMock(return_value=0)
        type(mock_popen).returncode = mock_returncode
        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)

        stdout, stderr, exitcodes = misc.rsync_remote_to_local(local_destination="./",
                                    id_file="~/.ssh/id_rsa",
                                    remote_user="user",
                                    remote_host="host",
                                    remote_source="/some/place/")

        self.assertEqual((stdout, stderr, exitcodes), ('hello mock subprocess stdout', 'hello mock subprocess stderr', 0))

        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called_once_with()


    def test_rsync_remote_to_local_with_mock_subprocess_failed(self):
        mock_popen = TestMisc.MockPopen()
        mock_popen.communicate = mock.Mock(return_value=('hello mock subprocess stdout', 'hello mock subprocess stderr'))
        mock_returncode = mock.PropertyMock(return_value=1)
        type(mock_popen).returncode = mock_returncode
        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)

        stdout, stderr, exitcodes = misc.rsync_remote_to_local(local_destination="./",
                                    id_file="~/.ssh/id_rsa",
                                    remote_user="user",
                                    remote_host="host",
                                    remote_source="/some/place/")

        self.assertEqual((stdout, stderr, exitcodes), ('hello mock subprocess stdout', 'hello mock subprocess stderr', 1))

        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called_once_with()


    def test_rsync_local_to_remote_with_mock_subprocess_successful(self):
        mock_popen = TestMisc.MockPopen()
        mock_popen.communicate = mock.Mock(return_value=('hello mock subprocess stdout', 'hello mock subprocess stderr'))
        mock_returncode = mock.PropertyMock(return_value=0)
        type(mock_popen).returncode = mock_returncode
        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)

        stdout, stderr, exitcodes = misc.rsync_local_to_remote(local_source="./",
                                    id_file="~/.ssh/id_rsa",
                                    remote_user="user",
                                    remote_host="host",
                                    remote_destination="/some/place/")

        self.assertEqual((stdout, stderr, exitcodes), ('hello mock subprocess stdout', 'hello mock subprocess stderr', 0))

        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called_once_with()


    def test_rsync_local_to_remote_with_mock_subprocess_failed(self):
        mock_popen = TestMisc.MockPopen()
        mock_popen.communicate = mock.Mock(return_value=('hello mock subprocess stdout', 'hello mock subprocess stderr'))
        mock_returncode = mock.PropertyMock(return_value=1)
        type(mock_popen).returncode = mock_returncode
        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)

        stdout, stderr, exitcodes = misc.rsync_local_to_remote(local_source="./",
                                    id_file="~/.ssh/id_rsa",
                                    remote_user="user",
                                    remote_host="host",
                                    remote_destination="/some/place/")

        self.assertEqual((stdout, stderr, exitcodes), ('hello mock subprocess stdout', 'hello mock subprocess stderr', 1))

        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called_once_with()


def main():
    unittest.main()

if __name__ == "__main__":
    main()

# EOF
