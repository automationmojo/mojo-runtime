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

from contextualize.exceptions import SemanticError

from contextualize.initialize import ContextAlias
from contextualize.variables import ActivationProfile, JobType, CONTEXTUALIZE_VARIABLES
from contextualize.xlogging.levels import LogLevel

__activation_profile__ = ActivationProfile.Console

# Guard against attemps to activate more than one, activation profile.
if CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE
    )
    raise SemanticError(errmsg)

CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE = ActivationProfile.Console
CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE = JobType.Console
os.environ[ContextAlias.CONTEXT_JOB_TYPE] = JobType.Console

if CONTEXTUALIZE_VARIABLES.CONTEXT_INTERACTIVE_CONSOLE:
    # If we are running in an interactive console, then we need to reduce the
    # console log level and we need to output log data to a console log file.

    temp_output_dir = tempfile.mkdtemp()

    # Only set the log levels if they were not previously set.  An option to a base
    # command may have set this in order to turn on a different level of verbosity
    if CONTEXTUALIZE_VARIABLES.CONTEXT_LOG_LEVEL_CONSOLE is None:
        CONTEXTUALIZE_VARIABLES.CONTEXT_LOG_LEVEL_CONSOLE = LogLevel.QUIET

    CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY = temp_output_dir

    # For console activation we don't want to log to the console and we want
    # to point the logs to a different output folder
    os.environ[ContextAlias.CONTEXT_CONSOLE_LOG_LEVEL] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_LOG_LEVEL_CONSOLE)
    os.environ[ContextAlias.CONTEXT_JOB_TYPE] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE)
    os.environ[ContextAlias.CONTEXT_OUTPUT_DIRECTORY] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY)

    import contextualize.activation.base # pylint: disable=unused-import,wrong-import-position

    from contextualize.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

    LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
    logging_initialize()

    def showlog():

        print("OUTPUT FOLDER: {}".format(CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY))
        print("")

        return

else:

    import contextualize.activation.base # pylint: disable=unused-import,wrong-import-position

    from contextualize.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

    LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
    logging_initialize()
