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
import subprocess

# Functions


def call_process(command):
    p = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    exitcodes = p.returncode

    return stdout, stderr, exitcodes


def say_hello_world():
    """Return the string "Hello World".

    This function returns the static string "Hello World".
    It is only a demo.

    Args:
        None

    Returns:
        str: "Hello World"

    :Example:

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

    :Example:
        Here are three Doctest :Example for usage of this function.

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
    >>> print(_get_numeric_logger_level_from_string("FOO_BAR"))
    10

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

        :arg str logger_name: name of logger for logfile name
        :arg console_log: to enable or disable
        :type console_log: True or False
        :arg str console_log_level: console log level (default "INFO")
        :arg file_log: to enable or disable file
        :type file_log: True or False
        :param str file_log_level: file log level (default "DEBUG")
        :param str file_log_dir: dir to write log file to. No trailing slash.
        :returns: logger
        :rtype: logging.Logger

    :Example:
        >>> print(set_up_logger()).level
        10
        >>> print(set_up_logger()).isEnabledFor(10)
        True
        >>> print(set_up_logger()).isEnabledFor(9)
        False

    That would be it.. File/Stream Handler might be interesting.

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


def rsync_local_to_remote(local_source=None,
                          id_file="~/.ssh/id_rsa",
                          remote_user="user",
                          remote_host="localhost",
                          remote_destination=None,
                          delete=False,
                          dry=False):
    """Rsync a given local file or directory to a remote ssh destination


    Args:
        local_source (str)        -- the local file/directory name
        id_file (str)             -- ssh private key file (id_rsa)
        remote_user (str)         -- username on remote host
        remote_host (str)         -- IP/FQDN of remote host
        remote_destination (str)  -- direcotry to put files on remote host
        delete (bool)             -- delete extraneous files from dest dirs
                            see rsync man page (default: False)
        dry (bool)                -- prints command string (rsync not executed)

    Returns:
        if dry is True:
            Return full rsync command string
        else:
            True|False, str -- if successful:   True, "ok"
                               if failed:       False, <Error Message>
    :Example:
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
        command_string = '''rsync -arq --inplace -e 'ssh -o BatchMode=yes \
-o UserKnownHostsFile="/dev/null" \
-o StrictHostKeyChecking=no -i "%(id_file)s"' %(local_source)s \
%(remote_user)s@%(remote_host)s:%(remote_destination)s''' % parameters
    else:
        command_string = '''rsync -arq --delete --inplace \
-e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" \
-o StrictHostKeyChecking=no -i "%(id_file)s"' %(local_source)s \
%(remote_user)s@%(remote_host)s:%(remote_destination)s''' % parameters

    if dry is True:
        return command_string
    else:
        stdout, stderr, exitcodes = call_process(command_string)

        if exitcodes == 0:
            print("rsync successful")
            #logger.info("rsync successful")
            return stdout, stderr, exitcodes
        else:
            print("rsync failed")
            #logger.error("rsync failed")
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
        local_destination (str)   -- the local file/directory name
        id_file (str)             -- ssh private key file (id_rsa)
        remote_user (str)         -- username on remote host
        remote_host (str)         -- IP/FQDN of remote host
        remote_source (str)       -- direcotry to put files on remote host
        delete (bool)             -- delete extraneous files from dest dirs
                            see rsync man page (default: False)
        dry (bool)                -- prints command string (rsync not executed)

    Returns:
        True|False, str -- if successful:   True, "ok"
                           if failed:       False, <Error Message>

    :Example:
        >>> print(rsync_remote_to_local(local_destination="./",
        ... id_file="~/.ssh/id_rsa", remote_user="user", remote_host="host",
        ... remote_source="/some/place/", delete=True, dry=True))
        rsync -arq --delete --inplace -e 'ssh -o BatchMode=yes -o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no -i "~/.ssh/id_rsa"' user@host:/some/place/ ./

        >>> print(rsync_remote_to_local(local_destination="./",
        ... id_file="~/.ssh/id_rsa", remote_user="user", remote_host="host",
        ... remote_source="/some/place/", dry=True))
        rsync -arq --inplace -e 'ssh -o BatchMode=yes \
-o UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no \
-i "~/.ssh/id_rsa"' user@host:/some/place/ ./

    """
    # todo make sure local_destination is ok..?!

    parameters = {'local_destination': local_destination,
                  'id_file': id_file,
                  'remote_user': remote_user,
                  'remote_host': remote_host,
                  'remote_source': remote_source}

    if delete is False:
        command_string = '''rsync -arq --inplace -e 'ssh -o BatchMode=yes -o \
UserKnownHostsFile="/dev/null" -o StrictHostKeyChecking=no \
-i "%(id_file)s"' %(remote_user)s@%(remote_host)s:%(remote_source)s \
%(local_destination)s''' % parameters
    else:
        command_string = '''rsync -arq --delete --inplace -e 'ssh \
-o BatchMode=yes -o UserKnownHostsFile="/dev/null" \
-o StrictHostKeyChecking=no -i "%(id_file)s"' \
%(remote_user)s@%(remote_host)s:%(remote_source)s \
%(local_destination)s''' % parameters

    if dry is True:
        return command_string
    else:
        stdout, stderr, exitcodes = call_process(command_string)

        if exitcodes == 0:
            #logger.info("rsync successful")
            print("rsync successful")
            return stdout, stderr, exitcodes
        else:
            #logger.error("rsync failed")
            print("rsync failed")
            return stdout, stderr, exitcodes





def main():
    """Main - this docstring count as vaild test :-)
    >>> main()

    """
    pass

if __name__ == "__main__":
    main()

# EOF
