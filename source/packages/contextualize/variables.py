"""
.. module:: variables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`CONTEXT_VARIABLES` object which is used store the environment variables.

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

from datetime import datetime
from enum import Enum

from contextualize.exceptions import SemanticError
from contextualize.initialize import CONTEXTUALIZE_OVERRIDES, ContextAlias
from contextualize.xdatetime import parse_datetime
from contextualize.xlogging.levels import LogLevel

class ActivationProfile(str, Enum):
    Command = "command"
    Console = "console"
    Orchestration = "orchestration"
    Service = "service"
    TestRun = "testrun"


class JobType(str, Enum):
    Unknown = "unknown"
    Console = "console"
    Service = "service"
    TestRun = "testrun"
    Orchestration = "orchestration"


def normalize_variable_whitespace(lval):
    lval = lval.strip().replace("/t", " ")
    while lval.find("  ") > -1:
        lval = lval.replace("  ", " ")
    return lval


class CONTEXTUALIZE_VARIABLES:
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    CONTEXT_STARTTIME = datetime.now()
    
    if CONTEXTUALIZE_OVERRIDES.CONTEXT_NAME is None:
        errmsg = "The `CONTEXT_NAME` override must be set by calling the " + \
            "`initialize_contextualize` function before importing this module."
        raise SemanticError(errmsg)
    CONTEXT_NAME = CONTEXTUALIZE_OVERRIDES.CONTEXT_NAME

    CONTEXT_LOGGER_NAME = CONTEXTUALIZE_OVERRIDES.CONTEXT_LOGGER_NAME

    CONTEXT_HOME_DIRECTORY = os.path.expanduser("~/{}".format(CONTEXT_NAME))
    
    CONTEXT_OUTPUT_DIRECTORY = os.path.expanduser("~/{}".format(CONTEXT_NAME))
    
    CONTEXT_USER_CONFIG_DIRECTORY = os.path.join(CONTEXT_HOME_DIRECTORY, "config")
    
    CONTEXT_USER_CONFIG_NAME = "user-runtime"
    
    CONTEXT_ACTIVATION_PROFILE = None
    
    CONTEXT_JOB_TYPE = JobType.Unknown
    
    CONTEXT_LOG_LEVEL_CONSOLE = LogLevel.WARNING

    CONTEXT_LOG_LEVEL_FILE = LogLevel.DEBUG

    CONTEXT_USER_CONFIG_FILENAME = os.path.join(CONTEXT_USER_CONFIG_DIRECTORY, "{}.yaml".format(CONTEXT_USER_CONFIG_NAME))

    CONTEXT_INTERACTIVE_CONSOLE = False

    CONTEXT_SERVICE_NAME = CONTEXTUALIZE_OVERRIDES.CONTEXT_SERVICE_NAME



def resolve_contextualize_variables():

    environ = os.environ

    if ContextAlias.CONTEXT_STARTTIME in environ:
        starttime = parse_datetime(environ[ContextAlias.CONTEXT_STARTTIME])
        CONTEXTUALIZE_VARIABLES.CONTEXT_STARTTIME = starttime

    CONTEXTUALIZE_VARIABLES.CONTEXT_HOME_DIRECTORY = os.path.expanduser(
        "~/{}".format(CONTEXTUALIZE_VARIABLES.CONTEXT_NAME))
    if ContextAlias.CONTEXT_HOME_DIRECTORY in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_HOME_DIRECTORY = environ[ContextAlias.CONTEXT_HOME_DIRECTORY]
    
    CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY = os.path.expanduser(
        "~/{}".format(CONTEXTUALIZE_VARIABLES.CONTEXT_NAME))
    if ContextAlias.CONTEXT_OUTPUT_DIRECTORY in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY = environ[ContextAlias.CONTEXT_OUTPUT_DIRECTORY]

    CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_DIRECTORY = os.path.join(
        CONTEXTUALIZE_VARIABLES.CONTEXT_HOME_DIRECTORY, "config")
    if ContextAlias.CONTEXT_USER_CONFIG_DIRECTORY in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_DIRECTORY = environ[ContextAlias.CONTEXT_USER_CONFIG_DIRECTORY]

    CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_NAME = "user-runtime"
    if ContextAlias.CONTEXT_USER_CONFIG_NAME in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_NAME = environ[ContextAlias.CONTEXT_USER_CONFIG_NAME]
    
    CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE = None
    if ContextAlias.CONTEXT_ACTIVATION_PROFILE in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE = environ[ContextAlias.CONTEXT_ACTIVATION_PROFILE]

    CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE = JobType.Unknown
    if ContextAlias.CONTEXT_JOB_TYPE in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE = environ[ContextAlias.CONTEXT_JOB_TYPE]

    CONTEXTUALIZE_VARIABLES.CONTEXT_INTERACTIVE_CONSOLE = False
    if ContextAlias.CONTEXT_INTERACTIVE_CONSOLE in environ:
        CONTEXTUALIZE_VARIABLES.CONTEXT_INTERACTIVE_CONSOLE = environ[ContextAlias.CONTEXT_INTERACTIVE_CONSOLE]

    CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_FILENAME = os.path.join(
        CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_DIRECTORY,
        "{}.yaml".format(CONTEXTUALIZE_VARIABLES.CONTEXT_USER_CONFIG_NAME))

    return