# -*- coding: utf-8 -*-
#
# Name:         misc.py
# Description:  Misc
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
__version_info__ = ('0', '4', '0')
__version__ = '.'.join(__version_info__)

# Imports
import logging
import os.path
import sys

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


def set_up_logger(logger_name="generic_logger",
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
            (default "generic_logger")

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
        log_file = file_log_dir + "/" + logger_name + ".log"
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


def main():
    pass

if __name__ == "__main__":
    main()

# EOF
