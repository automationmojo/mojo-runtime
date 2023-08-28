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

import os

from mojo.config.overrides import MOJO_CONFIG_OVERRIDES
from mojo.config.variables import MOJO_CONFIG_VARNAMES


class MOJO_RUNTIME_VARNAMES(MOJO_CONFIG_VARNAMES):
    MJR_ACTIVATION_PROFILE = "MJR_ACTIVATION_PROFILE"

    MJR_AUTOMATION_POD = "MJR_AUTOMATION_POD"

    MJR_BUILD_RELEASE = "MJR_BUILD_RELEASE"
    MJR_BUILD_BRANCH = "MJR_BUILD_BRANCH"
    MJR_BUILD_FLAVOR = "MJR_BUILD_FLAVOR"
    MJR_BUILD_NAME = "MJR_BUILD_NAME"
    MJR_BUILD_URL = "MJR_BUILD_URL"

    MJR_DEBUG_BREAKPOINTS = "MJR_DEBUG_BREAKPOINTS"
    MJR_DEBUG_DEBUGGER = "MJR_DEBUG_DEBUGGER"

    MJR_EXTENSION_FACTORY_ADDITIONS = "MJR_EXTENSION_FACTORY_ADDITIONS"

    MJR_INTERACTIVE_CONSOLE = "MJR_INTERACTIVE_CONSOLE"

    MJR_RUN_ID = "MJR_RUN_ID"

    MJR_PIPELINE_ID = "MJR_PIPELINE_ID"
    MJR_PIPELINE_NAME = "MJR_PIPELINE_NAME"
    MJR_PIPELINE_INSTANCE = "MJR_PIPELINE_INSTANCE"

    MJR_JOB_ID = "MJR_JOB_ID"
    MJR_JOB_INITIATOR = "MJR_JOB_INITIATOR"
    MJR_JOB_LABEL = "MJR_JOB_LABEL"
    MJR_JOB_NAME = "MJR_JOB_NAME"
    MJR_JOB_OWNER = "MJR_JOB_OWNER"
    MJR_JOB_TYPE = "MJR_JOB_TYPE"

    MJR_LOG_LEVEL_CONSOLE = "MJR_LOG_LEVEL_CONSOLE"
    MJR_LOG_LEVEL_FILE = "MJR_LOG_LEVEL_FILE"
    MJR_LOGGER_NAME = "MJR_LOGGER_NAME"

    MJR_OUTPUT_DIRECTORY = "MJR_OUTPUT_DIRECTORY"

    MJR_RESULTS_STATIC_SUMMARY_TEMPLATE = "MJR_RESULTS_STATIC_SUMMARY_TEMPLATE"
    MJR_RESULTS_STATIC_RESOURCE_DEST_DIR = "MJR_RESULTS_STATIC_RESOURCE_DEST_DIR"
    MJR_RESULTS_STATIC_RESOURCE_SRC_DIR = "MJR_RESULTS_STATIC_RESOURCE_SRC_DIR"

    MJR_SERVICE_NAME = "MJR_SERVICE_NAME"
    MJR_STARTTIME = "MJR_STARTTIME"

    MJR_TESTROOT = "MJR_TESTROOT"


class MOJO_RUNTIME_OVERRIDES(MOJO_CONFIG_OVERRIDES):

    MJR_LOGGER_NAME = "MJR"
    MJR_SERVICE_NAME = None


class MOJO_RUNTIME_STATE:
    INITIALIZED = False


def resolve_extension_factories():

    from mojo.runtime.variables import MOJO_RUNTIME_VARIABLES

    if MOJO_RUNTIME_VARIABLES.MJR_EXTENSION_FACTORY_ADDITIONS is not None:

        modules_raw = MOJO_RUNTIME_VARIABLES.MJR_EXTENSION_FACTORY_ADDITIONS.split(",")
        modules_trimmed = [nm.strip() for nm in modules_raw]

        from mojo.xmods.extension.configured import SuperFactory
        SuperFactory.search_modules.extend(modules_trimmed)

    return

def initialize_runtime(*, name: Optional[str]=None,
                          home_dir: Optional[str]=None,
                          logger_name: Optional[str]=None,
                          default_configuration: dict=None,
                          service_name: Optional[str]=None):

    MOJO_RUNTIME_STATE.INITIALIZED = True

    if name is not None:
        MOJO_CONFIG_OVERRIDES.MJR_NAME = name
        if home_dir is None:
            MOJO_CONFIG_OVERRIDES.MJR_HOME_DIRECTORY = os.path.join(os.path.expanduser("~"), name)
    if home_dir is not None:
        MOJO_CONFIG_OVERRIDES.MJR_HOME_DIRECTORY = os.path.expandvars(os.path.expanduser(home_dir))
    if logger_name is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_LOGGER_NAME = logger_name
    if default_configuration is not None:
        MOJO_CONFIG_OVERRIDES.DEFAULT_CONFIGURATION = default_configuration

    if service_name is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_SERVICE_NAME = service_name

    from mojo.runtime.variables import resolve_runtime_variables

    resolve_runtime_variables()

    resolve_extension_factories()

    return