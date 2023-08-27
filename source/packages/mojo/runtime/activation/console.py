"""
.. module:: console
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by interactive consoles to activate the environment
               with logging to the console minimized in order to provide a good interactive
               console work experience.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os
import tempfile

from logging.handlers import RotatingFileHandler

from mojo.errors.exceptions import SemanticError
from mojo.xmods.xlogging.levels import LogLevel

from mojo.runtime.initialize import MOJO_RUNTIME_VARNAMES
from mojo.runtime.variables import ActivationProfile, JobType, MOJO_RUNTIME_VARIABLES

__activation_profile__ = ActivationProfile.Console

# Guard against attemps to activate more than one, activation profile.
if MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE
    )
    raise SemanticError(errmsg)

MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = ActivationProfile.Console
MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Console.value
os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE

temp_output_dir = tempfile.mkdtemp()
MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = temp_output_dir

def showlog():

    print("OUTPUT FOLDER: {}".format(MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY))
    print("")

    return

if MOJO_RUNTIME_VARIABLES.MJR_INTERACTIVE_CONSOLE:
    # If we are running in an interactive console, then we need to reduce the
    # console log level and we need to output log data to a console log file.

    # Only set the log levels if they were not previously set.  An option to a base
    # command may have set this in order to turn on a different level of verbosity
    if MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE is None:
        MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE = LogLevel.QUIET

    # For console activation we don't want to log to the console and we want
    # to point the logs to a different output folder
    os.environ[MOJO_RUNTIME_VARNAMES.MJR_LOG_LEVEL_CONSOLE] = str(MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE)
    os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE
    os.environ[MOJO_RUNTIME_VARNAMES.MJR_OUTPUT_DIRECTORY] = str(MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY)

    import mojo.runtime.activation.base # pylint: disable=unused-import,wrong-import-position

    from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

    LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
    logging_initialize()

    showlog()

else:

    import mojo.runtime.activation.base # pylint: disable=unused-import,wrong-import-position

    from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

    LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
    logging_initialize()

    showlog()
