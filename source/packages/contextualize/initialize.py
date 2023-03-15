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


class ContextAlias:
    CONTEXT_NAME = "CONTEXT_NAME"
    CONTEXT_LOGGER_NAME = "CONTEXT_LOGGER_NAME"
    CONTEXT_STARTTIME = "CONTEXT_STARTTIME"
    CONTEXT_HOME_DIRECTORY = "CONTEXT_HOME_DIRECTORY"
    CONTEXT_OUTPUT_DIRECTORY = "CONTEXT_OUTPUT_DIRECTORY"
    CONTEXT_USER_CONFIG_DIRECTORY = "CONTEXT_USER_CONFIG_DIRECTORY"
    CONTEXT_USER_CONFIG_NAME = "CONTEXT_USER_CONFIG_NAME"
    CONTEXT_USER_CONFIG_FILENAME = "CONTEXT_USER_CONFIG_FILENAME"
    CONTEXT_ACTIVATION_PROFILE = "CONTEXT_ACTIVATION_PROFILE"
    CONTEXT_JOB_TYPE = "CONTEXT_JOB_TYPE"
    CONTEXT_CONSOLE_LOG_LEVEL = "CONTEXT_CONSOLE_LOG_LEVEL"
    CONTEXT_FILE_LOG_LEVEL = "CONTEXT_FILE_LOG_LEVEL"
    CONTEXT_INTERACTIVE_CONSOLE = "CONTEXT_INTERACTIVE_CONSOLE"
    CONTEXT_SERVICE_NAME = "CONTEXT_SERVICE_NAME"


class CONTEXTUALIZE_OVERRIDES:

    CONTEXT_NAME = None
    CONTEXT_LOGGER_NAME = None
    CONTEXT_SERVICE_NAME = None

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


def initialize_contextualize(*, name: str, logger_name: str, aliases: Type[ContextAlias]=ContextAlias,
        default_configuration: dict=CONTEXTUALIZE_OVERRIDES.DEFAULT_CONFIGURATION, service_name: Optional[str]=None):

    CONTEXTUALIZE_OVERRIDES.CONTEXT_NAME = name
    CONTEXTUALIZE_OVERRIDES.CONTEXT_LOGGER_NAME = logger_name

    ContextAlias.CONTEXT_STARTTIME = aliases.CONTEXT_STARTTIME
    ContextAlias.CONTEXT_HOME_DIRECTORY = aliases.CONTEXT_HOME_DIRECTORY
    ContextAlias.CONTEXT_OUTPUT_DIRECTORY = aliases.CONTEXT_OUTPUT_DIRECTORY
    ContextAlias.CONTEXT_USER_CONFIG_DIRECTORY = aliases.CONTEXT_USER_CONFIG_DIRECTORY
    ContextAlias.CONTEXT_USER_CONFIG_NAME = aliases.CONTEXT_USER_CONFIG_NAME
    ContextAlias.CONTEXT_ACTIVATION_PROFILE = aliases.CONTEXT_ACTIVATION_PROFILE
    ContextAlias.CONTEXT_JOB_TYPE = aliases.CONTEXT_JOB_TYPE
    ContextAlias.CONTEXT_CONSOLE_LOG_LEVEL = aliases.CONTEXT_CONSOLE_LOG_LEVEL
    ContextAlias.CONTEXT_FILE_LOG_LEVEL = aliases.CONTEXT_FILE_LOG_LEVEL
    ContextAlias.CONTEXT_INTERACTIVE_CONSOLE = aliases.CONTEXT_INTERACTIVE_CONSOLE
    ContextAlias.CONTEXT_SERVICE_NAME = aliases.CONTEXT_SERVICE_NAME

    CONTEXTUALIZE_OVERRIDES.DEFAULT_CONFIGURATION = default_configuration

    if service_name is not None:
        CONTEXTUALIZE_OVERRIDES.CONTEXT_SERVICE_NAME = service_name

    return
