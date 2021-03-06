# -*- coding: utf-8 -*-
#
# Name:         misc.py
# Description:  Misc
#
# Author:       mail@rhab.de
# Date:         1970-01-01

# Versioning
__version_info__ = ('0', '6', '3')
__version__ = '.'.join(__version_info__)

# Imports
import logging
import logging.handlers
import os.path
import sys
import subprocess

LOGGER_NAME = "log"
logger = logging.getLogger(LOGGER_NAME)

# Functions


def call_process(command):
    """Use subprocess Popen to execute system command. Return the result.

    Args:
        command (str):  complete string (raw?!) that should be executed

    Returns:
        str, str, int: Triple containing stdout, stderr, exitcodes

    Examples:
        None yet

    """

    process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exitcodes = process.returncode

    return stdout, stderr, exitcodes


def say_hello_world():
    """Return the string "Hello World".

    This function returns the static string "Hello World".
    It is only a demo.

    Args:
        None

    Returns:
        str: "Hello World"

    Example:
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
        name (str): Pass a name "Bob" in order to get "Hello Bob".
                    Again, just a demo.

    Returns:
        str: "Hello " + name

    Example:
        Here are three Doctests.

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
        level (str): the string representation of a logging level.
            Level is one of these:
            [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]

    Returns:
        int: value of the log level - see doctests below for mapping
            if for some reason the level is not known return DEBUG (10)

    Examples:
        Some doctests/exmamples:

        >>> print(_get_numeric_logger_level_from_string("NOTSET"))
        0
        >>> print(_get_numeric_logger_level_from_string("TRACE"))
        5
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
        >>> print(_get_numeric_logger_level_from_string("FOO_BAR"))
        10

    """

    if level == "NOTSET":
        return 0
    elif level == "TRACE":
        return 5
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
    **DEBUG log all levels.**
    The level sequence is: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
    Be aware that there are two layers for the logging level:

    1. the "core" logger level
    2. the "Handler" (either File or Stream) level.

    The core logger passes the messages on to the Handlers so the core level
    must at least match the most verbose Handler level.

    Args:
        logger_name (str):  name of logger for logfile name
        console_log (bool): to enable or disable
        console_log_level (str): console log level (default "INFO")
        file_log (bool):  to enable or disable file
        file_log_level (str): file log level (default "DEBUG")
        file_log_dir (str): dir to write log file to. No trailing slash.

    Returns:
        Logger: Object of Logger Class

    Notes:
        That would be it.. File/Stream Handler might be interesting.

    Examples:

        >>> print(set_up_logger()).level
        5
        >>> print(set_up_logger()).isEnabledFor(10)
        True
        >>> print(set_up_logger()).isEnabledFor(5)
        True
        >>> print(set_up_logger()).isEnabledFor(4)
        False

    """


    # instantiate logger object
    logger = logging.getLogger(logger_name)

    # add custom logger level "TRACE" (5)
    TRACE_LEVEL_NUM = 5
    logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
    def trace(self, message, *args, **kws):
        # Yes, logger takes its '*args' as 'args'.
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kws)
    logging.Logger.trace = trace

    # just set core level to TRACE (no need to evaluate file/console levels)
    logger.setLevel(_get_numeric_logger_level_from_string("TRACE"))

    # create formatter
    log_message_format = "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
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
        fh = logging.handlers.RotatingFileHandler(log_file, encoding='utf8',
                        maxBytes=10000000000, backupCount=5)
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


def rsync_local_to_remote(local_source=None,
                          id_file="~/.ssh/id_rsa",
                          remote_user="user",
                          remote_host="localhost",
                          remote_destination=None,
                          delete=False,
                          dry=False):
    """Rsync a given local file or directory to a remote ssh destination

    Args:
        local_source (str): the local file/directory name
        id_file (str): ssh private key file (id_rsa)
        remote_user (str): username on remote host
        remote_host (str): IP/FQDN of remote host
        remote_destination (str): direcotry to put files on remote host
        delete (bool): delete extraneous files from dest dirs
            see rsync man page (default: False)
        dry (bool): prints command string (rsync not executed)


    Returns:
        [str, str, int | str]: if dry is True: shell command string
            else: str, str, int: Triple containing stdout, stderr , exitcodes

    Examples:

        >>> print(rsync_local_to_remote(local_source="/some/foo", id_file="~/.ssh/id_rsa", remote_user="user", remote_host="host",remote_destination="/some/bar/", delete=True, dry=True))
        rsync -arq --delete --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "~/.ssh/id_rsa"' /some/foo user@host:/some/bar/

        >>> print(rsync_local_to_remote(local_source="/some/foo", id_file="~/.ssh/id_rsa", remote_user="user", remote_host="host", remote_destination="/some/bar/", dry=True))
        rsync -arq --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "~/.ssh/id_rsa"' /some/foo user@host:/some/bar/

    """

    parameters = {'local_source': local_source,
                  'id_file': id_file,
                  'remote_user': remote_user,
                  'remote_host': remote_host,
                  'remote_destination': remote_destination}

    if delete is False:
        command_string = '''rsync -arq --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "%(id_file)s"' %(local_source)s %(remote_user)s@%(remote_host)s:%(remote_destination)s''' % parameters
    else:
        command_string = '''rsync -arq --delete --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "%(id_file)s"' %(local_source)s %(remote_user)s@%(remote_host)s:%(remote_destination)s''' % parameters

    if dry is True:
        return command_string
    else:
        stdout, stderr, exitcodes = call_process(command_string)

        if exitcodes == 0:
            print "rsync successful"
            # logger.info("rsync successful")
            return stdout, stderr, exitcodes
        else:
            print "rsync failed"
            # logger.error("rsync failed")
            return stdout, stderr, exitcodes


def rsync_remote_to_local(local_destination=None,
                          id_file="~/.ssh/id_rsa",
                          remote_user="user",
                          remote_host="localhost",
                          remote_source=None,
                          delete=False,
                          dry=False):
    """Rsync a given remote file or directory to a local destination

    Args:
        local_destination (str): the local file/directory name
        id_file (str): ssh private key file (id_rsa)
        remote_user (str): username on remote host
        remote_host (str): IP/FQDN of remote host
        remote_source (str): direcotry to put files on remote host
        delete (bool): delete extraneous files from dest dirs
            see rsync man page (default: False)
        dry (bool): prints command string (rsync not executed)

    Returns:
        [str, str, int | str]: if dry is True: shell command string
            else: str, str, int: Triple containing stdout, stderr , exitcodes

    Examples:
        >>> print(rsync_remote_to_local(local_destination="./", id_file="~/.ssh/id_rsa", remote_user="user", remote_host="host", remote_source="/some/place/", delete=True, dry=True))
        rsync -arq --delete --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "~/.ssh/id_rsa"' user@host:/some/place/ ./

        >>> print(rsync_remote_to_local(local_destination="./", id_file="~/.ssh/id_rsa", remote_user="user", remote_host="host", remote_source="/some/place/", dry=True))
        rsync -arq --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "~/.ssh/id_rsa"' user@host:/some/place/ ./

    """

    # todo make sure local_destination is ok..?!

    parameters = {'local_destination': local_destination,
                  'id_file': id_file,
                  'remote_user': remote_user,
                  'remote_host': remote_host,
                  'remote_source': remote_source}

    if delete is False:
        command_string = '''rsync -arq --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "%(id_file)s"' %(remote_user)s@%(remote_host)s:%(remote_source)s %(local_destination)s''' % parameters
    else:
        command_string = '''rsync -arq --delete --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "%(id_file)s"' %(remote_user)s@%(remote_host)s:%(remote_source)s %(local_destination)s''' % parameters

    if dry is True:
        return command_string
    else:
        stdout, stderr, exitcodes = call_process(command_string)

        if exitcodes == 0:
            # logger.info("rsync successful")
            print "rsync successful"
            return stdout, stderr, exitcodes
        else:
            # logger.error("rsync failed")
            print "rsync failed"
            return stdout, stderr, exitcodes


def main():
    pass

if __name__ == "__main__":
    main()

# EOF
