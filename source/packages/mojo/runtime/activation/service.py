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

from logging.handlers import RotatingFileHandler

from mojo.xmods.xlogging.levels import LogLevel
from mojo.errors.exceptions import ConfigurationError, SemanticError

from mojo.runtime.initialize import MOJO_RUNTIME_VARNAMES
from mojo.runtime.variables import ActivationProfile, JobType, MOJO_RUNTIME_VARIABLES

__activation_profile__ = ActivationProfile.Service

# Guard against attemps to activate more than one, activation profile.
if MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE
    )
    raise SemanticError(errmsg)

MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = ActivationProfile.Service

service_name = MOJO_RUNTIME_VARIABLES.MJR_SERVICE_NAME

if service_name is None:
    if MOJO_RUNTIME_VARNAMES.MJR_SERVICE_NAME not in os.environ:
        errmsg = "To use the Mojo Runtime to provide a service, you must " \
                "set the '{}' environment variable.".format(MOJO_RUNTIME_VARNAMES.MJR_SERVICE_NAME)
        raise ConfigurationError(errmsg)

    service_name = os.environ[MOJO_RUNTIME_VARNAMES.MJR_SERVICE_NAME]

MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE = LogLevel.INFO
MOJO_RUNTIME_VARIABLES.MJR_SERVICE_NAME = service_name
MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Service.value
MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = "~/{}/services/{}".format(MOJO_RUNTIME_VARIABLES.MJR_NAME, service_name)

# For console activation we don't want to log to the console and we want
# to point the logs to a different output folder
os.environ[MOJO_RUNTIME_VARNAMES.MJR_LOG_LEVEL_CONSOLE] = str(MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE)
os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE
os.environ[MOJO_RUNTIME_VARNAMES.MJR_OUTPUT_DIRECTORY] = str(MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY)

import mojo.runtime.activation.base # pylint: disable=unused-import,wrong-import-position

from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
logging_initialize()
