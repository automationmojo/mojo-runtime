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

from mojo.runtime.initialize import MOJO_RUNTIME_OVERRIDES, MojoRuntimeAlias
from mojo.xmods.xexceptions import SemanticError
from mojo.xmods.xdatetime import parse_datetime
from mojo.xmods.xlogging.levels import LogLevel

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


class MOJO_RUNTIME_VARIABLES:
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    MJR_STARTTIME = datetime.now()
    
    if MOJO_RUNTIME_OVERRIDES.MJR_NAME is None:
        errmsg = "The `CONTEXT_NAME` override must be set by calling the " + \
            "`initialize_contextualize` function before importing this module."
        raise SemanticError(errmsg)
    MJR_NAME = MOJO_RUNTIME_OVERRIDES.MJR_NAME

    MJR_LOGGER_NAME = MOJO_RUNTIME_OVERRIDES.MJR_LOGGER_NAME

    MJR_HOME_DIRECTORY = os.path.expanduser("~/{}".format(MJR_NAME))
    
    MJR_OUTPUT_DIRECTORY = os.path.expanduser("~/{}".format(MJR_NAME))
    
    MJR_USER_CONFIG_DIRECTORY = os.path.join(MJR_HOME_DIRECTORY, "config")
    
    MJR_USER_CONFIG_NAME = "user-runtime"
    
    MJR_ACTIVATION_PROFILE = None
    
    MJR_JOB_TYPE = JobType.Unknown
    
    MJR_LOG_LEVEL_CONSOLE = LogLevel.WARNING

    MJR_LOG_LEVEL_FILE = LogLevel.DEBUG

    MJR_USER_CONFIG_FILENAME = os.path.join(MJR_USER_CONFIG_DIRECTORY, "{}.yaml".format(MJR_USER_CONFIG_NAME))

    MJR_INTERACTIVE_CONSOLE = False

    MJR_SERVICE_NAME = MOJO_RUNTIME_OVERRIDES.MJR_SERVICE_NAME



def resolve_contextualize_variables():

    environ = os.environ

    if MojoRuntimeAlias.MJR_STARTTIME in environ:
        starttime = parse_datetime(environ[MojoRuntimeAlias.MJR_STARTTIME])
        MOJO_RUNTIME_VARIABLES.MJR_STARTTIME = starttime

    MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY = os.path.expanduser(
        "~/{}".format(MOJO_RUNTIME_VARIABLES.MJR_NAME))
    if MojoRuntimeAlias.MJR_HOME_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY = environ[MojoRuntimeAlias.MJR_HOME_DIRECTORY]
    
    MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = os.path.expanduser(
        "~/{}".format(MOJO_RUNTIME_VARIABLES.MJR_NAME))
    if MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = environ[MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY]

    MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_DIRECTORY = os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "config")
    if MojoRuntimeAlias.MJR_USER_CONFIG_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_DIRECTORY = environ[MojoRuntimeAlias.MJR_USER_CONFIG_DIRECTORY]

    MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_NAME = "user-runtime"
    if MojoRuntimeAlias.MJR_USER_CONFIG_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_NAME = environ[MojoRuntimeAlias.MJR_USER_CONFIG_NAME]
    
    MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = None
    if MojoRuntimeAlias.MJR_ACTIVATION_PROFILE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = environ[MojoRuntimeAlias.MJR_ACTIVATION_PROFILE]

    MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Unknown
    if MojoRuntimeAlias.MJR_JOB_TYPE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = environ[MojoRuntimeAlias.MJR_JOB_TYPE]

    MOJO_RUNTIME_VARIABLES.MJR_INTERACTIVE_CONSOLE = False
    if MojoRuntimeAlias.MJR_INTERACTIVE_CONSOLE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_INTERACTIVE_CONSOLE = environ[MojoRuntimeAlias.MJR_INTERACTIVE_CONSOLE]

    MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_FILENAME = os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_DIRECTORY,
        "{}.yaml".format(MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_NAME))

    return