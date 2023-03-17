"""
.. module:: initialize
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains override mechanisms for the environment variable
               names used to initialize a global context for a python application

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

from typing import Optional, Type


class MojoRuntimeAlias:
    MJR_NAME = "MJR_NAME"
    MJR_LOGGER_NAME = "MJR_LOGGER_NAME"
    MJR_STARTTIME = "MJR_STARTTIME"
    MJR_HOME_DIRECTORY = "MJR_HOME_DIRECTORY"
    MJR_OUTPUT_DIRECTORY = "MJR_OUTPUT_DIRECTORY"
    MJR_USER_CONFIG_DIRECTORY = "MJR_USER_CONFIG_DIRECTORY"
    MJR_USER_CONFIG_NAME = "MJR_USER_CONFIG_NAME"
    MJR_USER_CONFIG_FILENAME = "MJR_USER_CONFIG_FILENAME"
    MJR_ACTIVATION_PROFILE = "MJR_ACTIVATION_PROFILE"
    MJR_JOB_TYPE = "MJR_JOB_TYPE"
    MJR_CONSOLE_LOG_LEVEL = "MJR_CONSOLE_LOG_LEVEL"
    MJR_FILE_LOG_LEVEL = "MJR_FILE_LOG_LEVEL"
    MJR_INTERACTIVE_CONSOLE = "MJR_INTERACTIVE_CONSOLE"
    MJR_SERVICE_NAME = "MJR_SERVICE_NAME"


class MOJO_RUNTIME_OVERRIDES:

    MJR_NAME = None
    MJR_LOGGER_NAME = None
    MJR_SERVICE_NAME = None

    DEFAULT_CONFIGURATION = { 
        "version": "1.0.0",
        "logging": {
            "levels": {
                "console": "INFO",
                "logfile": "DEBUG"
            },
            "logname": "{jobtype}.log",
        }
    }


def initialize_contextualize(*, name: str, logger_name: str, aliases: Type[MojoRuntimeAlias]=MojoRuntimeAlias,
        default_configuration: dict=MOJO_RUNTIME_OVERRIDES.DEFAULT_CONFIGURATION, service_name: Optional[str]=None):

    MOJO_RUNTIME_OVERRIDES.MJR_NAME = name
    MOJO_RUNTIME_OVERRIDES.MJR_LOGGER_NAME = logger_name

    MojoRuntimeAlias.MJR_STARTTIME = aliases.MJR_STARTTIME
    MojoRuntimeAlias.MJR_HOME_DIRECTORY = aliases.MJR_HOME_DIRECTORY
    MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY = aliases.MJR_OUTPUT_DIRECTORY
    MojoRuntimeAlias.MJR_USER_CONFIG_DIRECTORY = aliases.MJR_USER_CONFIG_DIRECTORY
    MojoRuntimeAlias.MJR_USER_CONFIG_NAME = aliases.MJR_USER_CONFIG_NAME
    MojoRuntimeAlias.MJR_ACTIVATION_PROFILE = aliases.MJR_ACTIVATION_PROFILE
    MojoRuntimeAlias.MJR_JOB_TYPE = aliases.MJR_JOB_TYPE
    MojoRuntimeAlias.MJR_CONSOLE_LOG_LEVEL = aliases.MJR_CONSOLE_LOG_LEVEL
    MojoRuntimeAlias.MJR_FILE_LOG_LEVEL = aliases.MJR_FILE_LOG_LEVEL
    MojoRuntimeAlias.MJR_INTERACTIVE_CONSOLE = aliases.MJR_INTERACTIVE_CONSOLE
    MojoRuntimeAlias.MJR_SERVICE_NAME = aliases.MJR_SERVICE_NAME

    MOJO_RUNTIME_OVERRIDES.DEFAULT_CONFIGURATION = default_configuration

    if service_name is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_SERVICE_NAME = service_name

    return
