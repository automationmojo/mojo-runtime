"""
.. module:: service
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by interactive services to activate the environment
               with logging to rotating logs much like what a persistant service would need.

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

from contextualize.xlogging.levels import LogLevel

from contextualize.exceptions import ConfigurationError, SemanticError
from contextualize.initialize import ContextAlias
from contextualize.variables import ActivationProfile, JobType, CONTEXTUALIZE_VARIABLES

__activation_profile__ = ActivationProfile.Service

# Guard against attemps to activate more than one, activation profile.
if CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE
    )
    raise SemanticError(errmsg)

CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE = ActivationProfile.Service

service_name = CONTEXTUALIZE_VARIABLES.CONTEXT_SERVICE_NAME

if service_name is None:
    if ContextAlias.CONTEXT_SERVICE_NAME not in os.environ:
        errmsg = "To use the AutomationKit to provide a service, you must " \
                "set the '{}' environment variable.".format(ContextAlias.CONTEXT_SERVICE_NAME)
        raise ConfigurationError(errmsg)

    service_name = os.environ[ContextAlias.CONTEXT_SERVICE_NAME]

CONTEXTUALIZE_VARIABLES.CONTEXT_LOG_LEVEL_CONSOLE = LogLevel.INFO
CONTEXTUALIZE_VARIABLES.CONTEXT_SERVICE_NAME = service_name
CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE = JobType.Service
CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY = "~/akit/services/{}".format(service_name)

# For console activation we don't want to log to the console and we want
# to point the logs to a different output folder
os.environ[ContextAlias.CONTEXT_CONSOLE_LOG_LEVEL] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_LOG_LEVEL_CONSOLE)
os.environ[ContextAlias.CONTEXT_JOB_TYPE] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE)
os.environ[ContextAlias.CONTEXT_OUTPUT_DIRECTORY] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_OUTPUT_DIRECTORY)

import contextualize.activation.base # pylint: disable=unused-import,wrong-import-position

from contextualize.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
logging_initialize()
