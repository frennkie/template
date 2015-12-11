from __future__ import unicode_literals
from __future__ import print_function

# Imports
import argparse
import sys
import logging
import logging.config

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)

####################################################
#### LOGGING DICTCONFIG SETTINGS (py27+, py32+) ####
####################################################
logger = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(name)s %(filename)s:%(lineno)d '
                      '%(levelname)s: %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "log/" + __file__ + ".log",
            'encoding': 'utf8',
            'maxBytes': 100000,
            'backupCount': 2,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)
#########################################
#### END LOGGING DICTCONFIG SETTINGS ####
#########################################


if __name__ == "__main__":

    # set up command line argument parsing
    parser = argparse.ArgumentParser(description="Else", epilog="Bar")
    parser.add_argument("-V", "--version",
                        help="print version", action="version",
                        version=__version__)
    parser.add_argument("-v", "--verbose",
                        help="console output high verbosity",
                        action="store_true")
    parser.add_argument("-q", "--quiet",
                        help="console output errors only",
                        action="store_true")
    parser.add_argument("--loglevel", type=str, default="DEBUG",
                        help="logfile verbosity (default: DEBUG)",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    # parse args
    args = parser.parse_args()


    print("ok...")
    logger.info("FYI")
    logger.error("error :-/")
    logger.debug("debug..")
    logger.setLevel(logging.INFO)
    logger.debug("debug2..")
    logger.info("info2..")

    logger.removeHandler('rotate_file')
    logger.debug("debug3..")

    logger.info("info3..")

