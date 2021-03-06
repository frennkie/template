#!venv/bin/python
# -*- coding: utf-8 -*-
"""This module does somthing

Explain what it does briefly. This can span over multiple lines. Not sure
whether and how to include meta data (Name, Author, Date)

- Name:         something.py
- Description:  Something
- Author:       mail@rhab.de
- Date:         1970-01-01
"""
# Versioning
__version_info__ = ('0', '6', '3')
__version__ = '.'.join(__version_info__)


""" Please remove this comment block after reading and understanding it:

This file contains templates for the following features:
1) Passing commandline parameters (arg) to the script
    - argmuents can be made either optional or mandatory
    - the option -h can not be used as this is implizit and prints a short help
    - argument type (string/int) and defaults can be defined

2) Logging
    a)  to console (two different facilities):
        - current user options:
            -V      print version (also --version)
            -v      very verbose (DEBUG)
            -q      very silent (ERROR)
        no flag regular (INFO)

    b) to file
        --loglevel
        --nolog     disable file logging

3) Exit codes for clear communication to calling scripts/users
    - e.g. sys.exit(os.EX_OK) for a clean exit
    - look for "os.EX_" for more: https://docs.python.org/2/library/os.html

4) Loading configuration settings from a file ("config.py")
    - check whether you need this
    - if yes, decide what happens if the file does not exist (pass or exit)

- remove until here!

"""


# Imports
import argparse
import sys

import modules.misc as misc

try:
    import config.config as config
except ImportError as error:
    # You! Need to decide what to do here.. exit or ignore and contiune!
    print "Could not import config.py. " + str(error)
    raise ImportError("Err Could not import config.py. Check config.py.sample")

    """
    # exit
    sys.exit(1)

    # pass
    continue
    """


# Same name as line 4 but without the extension (e.g. "backup_script")
SCRIPT_NAME = "something"
LOGGER_NAME = "log"

def fake():
    """Fake function so that we can run a fake test.

    Returns:
        result (bool): Always True

    Examples:

    >>> fake()
    True

    """

    return True


def main():
    """ Main """

    # set up command line argument parsing
    parser = argparse.ArgumentParser(description="Something")
    parser.add_argument("-V", "--version",
                        help="print version", action="version",
                        version=__version__)
    parser.add_argument("-v", "--verbose",
                        help="console output high verbosity",
                        action="store_true")
    parser.add_argument("-q", "--quiet",
                        help="console output errors only",
                        action="store_true")
    parser.add_argument("--nolog",
                        help="no log file (overrides --logdir and --loglevel)",
                        action="store_true")
    parser.add_argument("--logdir", type=str, default="log",
                        help="log dir (default: log)")
    parser.add_argument("--loglevel", type=str, default="DEBUG",
                        help="logfile verbosity (default: DEBUG)",
                        choices=['TRACE', 'DEBUG',
                                 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    # parse args
    args = parser.parse_args()

    # -q (quiet) has precedence over -v (verbose)
    if args.quiet:
        args_verbosity = "ERROR"
    else:
        # if -q is not set check for -v (verbose). If not set default to "INFO"
        if args.verbose:
            args_verbosity = "DEBUG"
        else:
            args_verbosity = "INFO"

    if args.nolog:
        logger = misc.set_up_logger(logger_name=LOGGER_NAME,
                                    console_log=True,
                                    console_log_level=args_verbosity,
                                    file_log=False)
    else:
        logger = misc.set_up_logger(logger_name=LOGGER_NAME,
                                    console_log=True,
                                    console_log_level=args_verbosity,
                                    file_log=True,
                                    file_log_level=args.loglevel,
                                    file_log_dir=args.logdir)

    print "loglevel: " + args.loglevel
    logger.trace("trace message")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")

    logger.info(__name__)

    """
    print config.PASSWORD
    print misc.say_hello_world()
    """
    # Start Coding Here!

    misc.say_hello_world()

if __name__ == "__main__":
    main()

# EOF
