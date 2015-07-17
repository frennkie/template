#!/bin/sh
#
# Name:         clean_pyc.sh
# Description:  Delete *.pyc files and __pycache__ directories
#
# Author:       mail@rhab.de
# Date:         1970-01-01

DIR=`pwd | egrep ".*/template/template$"`
RESULT=$?

# note: single = is dash (/bin/sh) style
if [ ${RESULT} -eq 0 ]; then
    find ./ -type f -iname '*.pyc' -not -path "./venv/*" -delete
    find ./ -type d -iname '__pycache__' -not -path "./venv/*" -delete
    echo "done cleaning up"
else
    echo "I'd like to be run from /home/XXX/template/template"
fi

#EOF
