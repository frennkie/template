#!venv/bin/python
# -*- coding: utf-8 -*-
#
# Name:         something.py
# Description:  Something
#
# Author:       mail@rhab.de
# Date:         1970-01-01

### Versioning
__version_info__ = ('0', '1', 'dev2')
__version__ = '.'.join(__version_info__)

### Imports
#import config.config as config
import config

def main():
    print config.PASSWORD

if __name__ == "__main__":
    main()

#EOF
