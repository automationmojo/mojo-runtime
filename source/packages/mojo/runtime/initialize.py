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
    MJR_ACTIVATION_PROFILE = "MJR_ACTIVATION_PROFILE"

    MJR_AUTOMATION_POD = "MJR_AUTOMATION_POD"

    MJR_BUILD_RELEASE = "MJR_BUILD_RELEASE"
    MJR_BUILD_BRANCH = "MJR_BUILD_BRANCH"
    MJR_BUILD_FLAVOR = "MJR_BUILD_FLAVOR"
    MJR_BUILD_NAME = "MJR_BUILD_NAME"
    MJR_BUILD_URL = "MJR_BUILD_URL"

    MJR_CONFIG_CREDENTIAL_NAMES = "MJR_CONFIG_CREDENTIAL_NAMES"
    MJR_CONFIG_CREDENTIAL_FILES = "MJR_CONFIG_CREDENTIAL_FILES"
    MJR_CONFIG_CREDENTIAL_SEARCH_PATHS = "MJR_CONFIG_CREDENTIAL_SEARCH_PATHS"
    MJR_CONFIG_DIRECTORY = "MJR_CONFIG_DIRECTORY"
    MJR_CONFIG_LANDSCAPE_NAMES = "MJR_CONFIG_LANDSCAPE_NAMES"
    MJR_CONFIG_LANDSCAPE_FILES = "MJR_CONFIG_LANDSCAPE_NAMES"
    MJR_CONFIG_LANDSCAPE_SEARCH_PATHS = "MJR_CONFIG_LANDSCAPE_SEARCH_PATHS"
    MJR_CONFIG_RUNTIME_NAMES = "MJR_CONFIG_RUNTIME_NAMES"
    MJR_CONFIG_RUNTIME_FILES = "MJR_CONFIG_RUNTIME_PATHS"
    MJR_CONFIG_RUNTIME_SEARCH_PATHS = "MJR_CONFIG_RUNTIME_SEARCH_PATHS"
    MJR_CONFIG_TOPOLOGY_NAMES = "MJR_CONFIG_TOPOLOGY_NAMES"
    MJR_CONFIG_TOPOLOGY_FILES = "MJR_CONFIG_TOPOLOGY_FILES"
    MJR_CONFIG_TOPOLOGY_SEARCH_PATHS = "MJR_CONFIG_TOPOLOGY_SEARCH_PATHS"

    MJR_DEBUG_BREAKPOINTS = "MJR_DEBUG_BREAKPOINTS"
    MJR_DEBUG_DEBUGGER = "MJR_DEBUG_DEBUGGER"

    MJR_EXTENSION_FACTORY_ADDITIONS = "MJR_EXTENSION_FACTORY_ADDITIONS"

    MJR_HOME_DIRECTORY = "MJR_HOME_DIRECTORY"

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

    MJR_NAME = "MJR_NAME"

    MJR_OUTPUT_DIRECTORY = "MJR_OUTPUT_DIRECTORY"

    MJR_RESULTS_STATIC_SUMMARY_TEMPLATE = "MJR_RESULTS_STATIC_SUMMARY_TEMPLATE"
    MJR_RESULTS_STATIC_RESOURCE_DEST_DIR = "MJR_RESULTS_STATIC_RESOURCE_DEST_DIR"
    MJR_RESULTS_STATIC_RESOURCE_SRC_DIR = "MJR_RESULTS_STATIC_RESOURCE_SRC_DIR"

    MJR_SERVICE_NAME = "MJR_SERVICE_NAME"
    MJR_STARTTIME = "MJR_STARTTIME"

    MJR_TESTROOT = "MJR_TESTROOT"

    MJR_USER_CONFIG_DIRECTORY = "MJR_USER_CONFIG_DIRECTORY"
    MJR_USER_CONFIG_NAME = "MJR_USER_CONFIG_NAME"
    MJR_USER_CONFIG_FILENAME = "MJR_USER_CONFIG_FILENAME"


class MOJO_RUNTIME_OVERRIDES:

    MJR_NAME = "mjr"

    MJR_LOGGER_NAME = "MJR"
    MJR_SERVICE_NAME = None

    MJR_CONFIG_USE_CREDENTIALS = False
    MJR_CONFIG_USE_LANDSCAPE = False
    MJR_CONFIG_USE_RUNTIME = False
    MJR_CONFIG_USE_TOPOLOGY = False

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
                          logger_name: Optional[str]=None,
                          use_credential: Optional[bool]=None,
                          use_landscape: Optional[bool]=None,
                          use_runtime: Optional[bool]=None,
                          use_topology: Optional[bool]=None,
                          default_configuration: dict=None,
                          service_name: Optional[str]=None):

    MOJO_RUNTIME_STATE.INITIALIZED = True

    if name is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_NAME = name
    if logger_name is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_LOGGER_NAME = logger_name
    if use_credential is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS = use_credential
    if use_landscape is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE = use_landscape
    if use_runtime is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_RUNTIME = use_runtime
    if use_topology is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY = use_topology
    if default_configuration is not None:
        MOJO_RUNTIME_OVERRIDES.DEFAULT_CONFIGURATION = default_configuration

    if service_name is not None:
        MOJO_RUNTIME_OVERRIDES.MJR_SERVICE_NAME = service_name

    from mojo.runtime.variables import resolve_runtime_variables

    resolve_runtime_variables()

    resolve_extension_factories()

    return