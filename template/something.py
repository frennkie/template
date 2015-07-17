#!venv/bin/python
# -*- coding: utf-8 -*-
#
# Name:         something.py
# Description:  Something
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
__version_info__ = ('0', '2', '1')
__version__ = '.'.join(__version_info__)

# Imports
import argparse
import logging
import os.path
import sys

import config.config as config
import modules.misc as misc


# Same name as line 4 but without the extension (e.g. "backup_script")
script_name = "something"


def _get_numeric_logger_level_from_string(level):
    """Parse string and return appropriate numeric logger level

    Args:
        level (str)     -- the string representation of a logging level.
            Level is one of these: [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]

    Returns:
        int value of the log level - see doctests below for mapping
            if for some reason the level is not known return DEBUG (10)

    >>> print(_get_numeric_logger_level_from_string("NOTSET"))
    0
    >>> print(_get_numeric_logger_level_from_string("DEBUG"))
    10
    >>> print(_get_numeric_logger_level_from_string("INFO"))
    20
    >>> print(_get_numeric_logger_level_from_string("WARNING"))
    30
    >>> print(_get_numeric_logger_level_from_string("ERROR"))
    40
    >>> print(_get_numeric_logger_level_from_string("CRITICAL"))
    50

    """

    if level == "NOTSET":
        return 0
    elif level == "DEBUG":
        return 10
    elif level == "INFO":
        return 20
    elif level == "WARNING":
        return 30
    elif level == "ERROR":
        return 40
    elif level == "CRITICAL":
        return 50
    else:
        return 10


def set_up_logger(logger_name=script_name,
                  console_log=True,
                  console_log_level="INFO",
                  file_log=True,
                  file_log_level="DEBUG",
                  file_log_dir="log"):
    """Set up an instance of logging for both file and console logs.

        Log level ERROR contains ERROR and CRITICAL.
        WARNING contains ERROR (and CRITICAL) and so on.
        DEBUG log all levels.
        The level sequence is: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        Be aware that there are two layers for the logging level:
        1) the "core" logger level
        2) the "Handler" (either File or Stream) level.
        The core logger passes the messages on to the Handlers so the core
        level must at least match the most verbose Handler level.

    Args:
        logger_name (str)       -- name of logger for logfile name
            (default script_name) - script_name is a global variable

        console_log (bool)      -- [True|False] to enable or disable
            console logging (default True)

        console_log_level (str) -- console log level (default "INFO")

        file_log (bool)         -- [True|False] to enable or disable file
            logging (default True)

        file_log_level (str)    -- file log level (default "DEBUG")

        file_log_dir (str)      -- dir to write log file to. No trailing slash.
             (default "log")

    Returns:
        logger object

    """

    # instantiate logger object
    logger = logging.getLogger(logger_name)

    # just set core level to DEBUG (no need to evaluate file/console levels)
    logger.setLevel(_get_numeric_logger_level_from_string("DEBUG"))

    # create formatter
    log_message_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_message_format)

    # is file logging enabled?
    if file_log is True:
        # make sure file_log_dir exists and we can write to it
        if not os.path.exists(file_log_dir):
            try:
                os.makedirs(file_log_dir)
            except IOError, e:
                print "IOError: Can't create log dir " + file_log_dir
                print e
                sys.exit(1)
            except Exception, e:
                print "Generic Error: Can't create log dir " + file_log_dir
                print e
                sys.exit(1)

        # construct relative path and name of log file and try to write to it
        log_file = file_log_dir + "/" + script_name + ".log"
        try:
            open(log_file, 'a')
        except IOError, e:
            print "IOError: Can't write to log file " + log_file
            print e
            sys.exit(1)
        except Exception, e:
            print "Generic Error: Can't write to log file " + log_file
            print e
            sys.exit(1)

        # add FileHandler, set Level, add Formatter, apply Handler to logger
        fh = logging.FileHandler(log_file)
        fh.setLevel(_get_numeric_logger_level_from_string(file_log_level))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    else:
        # file logging disabled
        pass

    # is console logging enabled?
    if console_log is True:
        # add StreamHandler, set Level, add Formatter, apply Handler to logger
        ch = logging.StreamHandler()
        ch.setLevel(_get_numeric_logger_level_from_string(console_log_level))
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    else:
        # console logging is disabled
        pass

    # return logger object
    return logger


def fake():
    return True


def main():
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
                        choices=['DEBUG',
                                 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    # parse args
    args = parser.parse_args()

    # -q (quite) has precedence over -v (verbose)
    if args.quiet:
        args_verbosity = "ERROR"
    else:
        # if -q is not set check for -v (verbose). If not set default to "INFO"
        if args.verbose:
            args_verbosity = "DEBUG"
        else:
            args_verbosity = "INFO"

    if args.nolog:
        logger = set_up_logger(console_log=True,
                               console_log_level=args_verbosity,
                               file_log=False)
    else:
        logger = set_up_logger(console_log=True,
                               console_log_level=args_verbosity,
                               file_log=True,
                               file_log_level=args.loglevel,
                               file_log_dir=args.logdir)

    # sample loggings
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")

    # sample config access
    print config.PASSWORD
    # sample modules access
    print misc.say_hello_world()

    # start your code here

if __name__ == "__main__":
    main()

# EOF
