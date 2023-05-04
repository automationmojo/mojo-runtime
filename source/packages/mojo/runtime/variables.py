"""
.. module:: variables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`MOJO_RUNTIME_VARIABLES`
              object which is used store the environment variables.

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

from typing import List

import os

from datetime import datetime
from enum import Enum

from mojo.runtime.initialize import MOJO_RUNTIME_OVERRIDES, MojoRuntimeAlias
from mojo.xmods.exceptions import ConfigurationError, SemanticError
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


class DefaultValue:
    NotSet = "(not-set)"

class MOJO_RUNTIME_VARIABLES:
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    MJR_NAME = MOJO_RUNTIME_OVERRIDES.MJR_NAME

    MJR_SERVICE_NAME = MOJO_RUNTIME_OVERRIDES.MJR_SERVICE_NAME
    MJR_LOGGER_NAME = MOJO_RUNTIME_OVERRIDES.MJR_LOGGER_NAME

    MJR_HOME_DIRECTORY = os.path.expanduser("~/{}".format(MJR_NAME))   
    MJR_OUTPUT_DIRECTORY = None
    
    MJR_ACTIVATION_PROFILE = None
    
    MJR_AUTOMATION_POD = DefaultValue.NotSet

    MJR_BUILD_BRANCH = DefaultValue.NotSet
    MJR_BUILD_FLAVOR = DefaultValue.NotSet
    MJR_BUILD_NAME = DefaultValue.NotSet
    MJR_BUILD_URL = DefaultValue.NotSet

    MJR_CONFIG_DIRECTORY = None
    MJR_CONFIG_CREDENTIAL_NAMES = None
    MJR_CONFIG_CREDENTIAL_FILES = None
    MJR_CONFIG_CREDENTIAL_SEARCH_PATHS = None
    MJR_CONFIG_LANDSCAPE_NAMES = None
    MJR_CONFIG_LANDSCAPE_FILES = None
    MJR_CONFIG_LANDSCAPE_SEARCH_PATHS = None
    MJR_CONFIG_RUNTIME_NAMES = None
    MJR_CONFIG_RUNTIME_FILES = None
    MJR_CONFIG_RUNTIME_SEARCH_PATHS = None
    MJR_CONFIG_TOPOLOGY_NAMES = None
    MJR_CONFIG_TOPOLOGY_FILES = None
    MJR_CONFIG_TOPOLOGY_SEARCH_PATHS = None

    MJR_DEBUG_BREAKPOINTS = None
    MJR_DEBUG_DEBUGGER = None

    MJR_INTERACTIVE_CONSOLE = False

    MJR_JOB_ID = DefaultValue.NotSet
    MJR_JOB_TYPE = JobType.Unknown
    MJR_JOB_INITIATOR = DefaultValue.NotSet
    MJR_JOB_LABEL = DefaultValue.NotSet
    MJR_JOB_NAME = DefaultValue.NotSet
    MJR_JOB_OWNER = DefaultValue.NotSet
    
    MJR_LOG_LEVEL_CONSOLE = LogLevel.WARNING
    MJR_LOG_LEVEL_FILE = LogLevel.DEBUG

    MJR_RESULTS_STATIC_SUMMARY_TEMPLATE = None
    MJR_RESULTS_STATIC_RESOURCE_DEST_DIR = None
    MJR_RESULTS_STATIC_RESOURCE_SRC_DIR = None

    MJR_STARTTIME = datetime.now()

    MJR_TESTROOT = None

    MJR_USER_CONFIG_DIRECTORY = os.path.join(MJR_HOME_DIRECTORY, "config")
    MJR_USER_CONFIG_NAME = "user-runtime"
    MJR_USER_CONFIG_FILENAME = os.path.join(MJR_USER_CONFIG_DIRECTORY, "{}.yaml".format(MJR_USER_CONFIG_NAME))

def normalize_name_list(names: str, sep: str=","):
    norm_names: List[str] = []

    cand_names: List[str] = os.path.split(names, sep)
    for nxt_name in cand_names:
        nname = nxt_name.strip()
        norm_names.append(nname)
    
    return norm_names

def normalize_path_list(paths: str, sep: str=";"):
    norm_paths: List[str] = []

    search_paths: List[str] = os.path.split(paths, sep)
    for nxt_path in search_paths:
        nxt_full_path = os.path.abspath(os.path.expandvars(os.path.expanduser(nxt_path.strip())))
        norm_paths.append(nxt_full_path)

    return norm_paths

def resolve_config_files(config_type: str, config_names: List[str], search_path: List[str]):
    config_files = []
    missing_files = []

    for chk_name in config_names:
        found_filename = None
        for chk_path in search_path:
            chk_basename = f"{chk_name}.yaml"
            chk_filename = os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(chk_path, chk_basename))))
            if os.path.exists(chk_filename):
                found_filename = chk_filename
                break
        
        if found_filename is not None:
            config_files.append(found_filename)
        else:
            missing_files.append(chk_name)

    if len(missing_files) > 0:
        errmsg_lines = [
            f"Error loading {config_type} configuration files.",
            "FILENAMES:"
        ]

        for chk_name in config_names:
            errmsg_lines.append(f"    {chk_name}")
        
        errmsg_lines.append("SEARCH PATHS:")
        for chk_path in search_path:
            errmsg_lines.append(f"    {chk_path}")

        errmsg = os.path.join(errmsg_lines)
        raise ConfigurationError(errmsg)

    return config_files


def resolve_runtime_variables():

    environ = os.environ


    from mojo.xmods.xcollections.context import Context, ContextPaths

    ctx = Context()

    if MojoRuntimeAlias.MJR_STARTTIME in environ:
        starttime = parse_datetime(environ[MojoRuntimeAlias.MJR_STARTTIME])
        MOJO_RUNTIME_VARIABLES.MJR_STARTTIME = starttime

    MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY = os.path.expanduser(
        "~/{}".format(MOJO_RUNTIME_VARIABLES.MJR_NAME))
    if MojoRuntimeAlias.MJR_HOME_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY = environ[MojoRuntimeAlias.MJR_HOME_DIRECTORY]
    
    MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = None
    if MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = environ[MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY]

    MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = None
    if MojoRuntimeAlias.MJR_ACTIVATION_PROFILE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = environ[MojoRuntimeAlias.MJR_ACTIVATION_PROFILE]

    MOJO_RUNTIME_VARIABLES.MJR_AUTOMATION_POD = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_AUTOMATION_POD in environ:
        MOJO_RUNTIME_VARIABLES.MJR_AUTOMATION_POD = environ[MojoRuntimeAlias.MJR_AUTOMATION_POD]

    MOJO_RUNTIME_VARIABLES.MJR_BUILD_BRANCH = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_BRANCH in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_BRANCH = environ[MojoRuntimeAlias.MJR_BUILD_BRANCH]
    
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_NAME = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_NAME = environ[MojoRuntimeAlias.MJR_BUILD_NAME]
    
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_FLAVOR = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_FLAVOR in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_FLAVOR = environ[MojoRuntimeAlias.MJR_BUILD_FLAVOR]

    MOJO_RUNTIME_VARIABLES.MJR_BUILD_URL = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_URL in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_URL = environ[MojoRuntimeAlias.MJR_BUILD_URL]

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_DIRECTORY = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "config")
    if MojoRuntimeAlias.MJR_CONFIG_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_DIRECTORY = environ[MojoRuntimeAlias.MJR_CONFIG_DIRECTORY]

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES = ["credentials"]
    if MojoRuntimeAlias.MJR_CONFIG_CREDENTIAL_NAMES in environ:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS = True
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES = normalize_name_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_CREDENTIAL_NAMES])
    
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_SEARCH_PATHS = [os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_DIRECTORY)]
    if MojoRuntimeAlias.MJR_CONFIG_CREDENTIAL_SEARCH_PATHS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_SEARCH_PATHS = normalize_path_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_CREDENTIAL_SEARCH_PATHS])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES = ["default-landscape"]
    if MojoRuntimeAlias.MJR_CONFIG_LANDSCAPE_NAMES in environ:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE = True
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES = normalize_name_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_LANDSCAPE_NAMES])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_SEARCH_PATHS = [os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_DIRECTORY, "landscapes")]
    if MojoRuntimeAlias.MJR_CONFIG_LANDSCAPE_SEARCH_PATHS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_SEARCH_PATHS = normalize_path_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_LANDSCAPE_SEARCH_PATHS])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_NAMES = ["default-runtime"]
    if MojoRuntimeAlias.MJR_CONFIG_RUNTIME_NAMES in environ:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_RUNTIME = True
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_NAMES = normalize_name_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_RUNTIME_NAMES])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_SEARCH_PATHS = [os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_DIRECTORY, "runtimes")]
    if MojoRuntimeAlias.MJR_CONFIG_RUNTIME_SEARCH_PATHS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_SEARCH_PATHS = normalize_path_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_RUNTIME_SEARCH_PATHS])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES = ["default-topology"]
    if MojoRuntimeAlias.MJR_CONFIG_TOPOLOGY_NAMES in environ:
        MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY = True
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES = normalize_name_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_TOPOLOGY_NAMES])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_SEARCH_PATHS = [os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_DIRECTORY, "topologies")]
    if MojoRuntimeAlias.MJR_CONFIG_TOPOLOGY_SEARCH_PATHS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_SEARCH_PATHS = normalize_path_list(
            environ[MojoRuntimeAlias.MJR_CONFIG_TOPOLOGY_SEARCH_PATHS])

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_FILES = []
    if MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS:
        config_names = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES
        if len(config_names) == 0:
            config_names = ["credentials"]
        search_paths = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_SEARCH_PATHS
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_FILES = resolve_config_files("credential", config_names, search_paths)
        ctx.insert(ContextPaths.CONFIG_CREDENTIAL_FILES, MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_FILES)

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_FILES = []
    if MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE:
        config_names = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES
        if len(config_names) == 0:
            config_names = ["default-landscape"]
        search_paths = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_SEARCH_PATHS
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_FILES = resolve_config_files("landscape", config_names, search_paths)
        ctx.insert(ContextPaths.CONFIG_LANDSCAPE_FILES, MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_FILES)

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_FILES = []
    if MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_RUNTIME:
        config_names = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_NAMES
        if len(config_names) == 0:
            config_names = ["default-runtime"]
        search_paths = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_SEARCH_PATHS
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_FILES = resolve_config_files("runtime", config_names, search_paths)
        ctx.insert(ContextPaths.CONFIG_RUNTIME_FILES, MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_FILES)

    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_FILES = []
    if MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY:
        config_names = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES
        if len(config_names) == 0:
            config_names = ["default-topology"]
        search_paths = MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_SEARCH_PATHS
        MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_FILES = resolve_config_files("topology", config_names, search_paths)
        ctx.insert(ContextPaths.CONFIG_TOPOLOGY_FILES, MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_FILES)

    MOJO_RUNTIME_VARIABLES.MJR_DEBUG_BREAKPOINTS = None
    if MojoRuntimeAlias.MJR_DEBUG_BREAKPOINTS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_DEBUG_BREAKPOINTS = environ[MojoRuntimeAlias.MJR_DEBUG_BREAKPOINTS]

    MOJO_RUNTIME_VARIABLES.MJR_DEBUG_DEBUGGER = None
    if MojoRuntimeAlias.MJR_DEBUG_DEBUGGER in environ:
        MOJO_RUNTIME_VARIABLES.MJR_DEBUG_DEBUGGER = environ[MojoRuntimeAlias.MJR_DEBUG_DEBUGGER]
    
    MOJO_RUNTIME_VARIABLES.MJR_EXTENSION_FACTORY_ADDITIONS = None
    if MojoRuntimeAlias.MJR_EXTENSION_FACTORY_ADDITIONS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_EXTENSION_FACTORY_ADDITIONS = environ[MojoRuntimeAlias.MJR_EXTENSION_FACTORY_ADDITIONS]

    MOJO_RUNTIME_VARIABLES.MJR_JOB_ID = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_ID in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_ID = environ[MojoRuntimeAlias.MJR_JOB_ID]

    MOJO_RUNTIME_VARIABLES.MJR_JOB_INITIATOR = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_INITIATOR in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_INITIATOR = environ[MojoRuntimeAlias.MJR_JOB_INITIATOR]
    
    MOJO_RUNTIME_VARIABLES.MJR_JOB_LABEL = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_LABEL in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_LABEL = environ[MojoRuntimeAlias.MJR_JOB_LABEL]
    
    MOJO_RUNTIME_VARIABLES.MJR_JOB_NAME = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_NAME = environ[MojoRuntimeAlias.MJR_JOB_NAME]

    MOJO_RUNTIME_VARIABLES.MJR_JOB_OWNER = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_OWNER in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_OWNER = environ[MojoRuntimeAlias.MJR_JOB_OWNER]

    MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Unknown
    if MojoRuntimeAlias.MJR_JOB_TYPE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = environ[MojoRuntimeAlias.MJR_JOB_TYPE]

    MOJO_RUNTIME_VARIABLES.MJR_INTERACTIVE_CONSOLE = False
    if MojoRuntimeAlias.MJR_INTERACTIVE_CONSOLE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_INTERACTIVE_CONSOLE = environ[MojoRuntimeAlias.MJR_INTERACTIVE_CONSOLE]

    MOJO_RUNTIME_VARIABLES.MJR_RESULTS_STATIC_SUMMARY_TEMPLATE = None
    if MojoRuntimeAlias.MJR_RESULTS_STATIC_SUMMARY_TEMPLATE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_RESULTS_STATIC_SUMMARY_TEMPLATE = environ[MojoRuntimeAlias.MJR_RESULTS_STATIC_SUMMARY_TEMPLATE]

    MOJO_RUNTIME_VARIABLES.MJR_RESULTS_STATIC_RESOURCE_DEST_DIR = None
    if MojoRuntimeAlias.MJR_RESULTS_STATIC_RESOURCE_DEST_DIR in environ:
        MOJO_RUNTIME_VARIABLES.MJR_RESULTS_STATIC_RESOURCE_DEST_DIR = environ[MojoRuntimeAlias.MJR_RESULTS_STATIC_RESOURCE_DEST_DIR]
    
    MOJO_RUNTIME_VARIABLES.MJR_RESULTS_STATIC_RESOURCE_SRC_DIR = None
    if MojoRuntimeAlias.MJR_RESULTS_STATIC_RESOURCE_SRC_DIR in environ:
        MOJO_RUNTIME_VARIABLES.MJR_RESULTS_STATIC_RESOURCE_SRC_DIR = environ[MojoRuntimeAlias.MJR_RESULTS_STATIC_RESOURCE_SRC_DIR]

    MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_DIRECTORY = os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "config")
    if MojoRuntimeAlias.MJR_USER_CONFIG_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_DIRECTORY = environ[MojoRuntimeAlias.MJR_USER_CONFIG_DIRECTORY]

    MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_NAME = "user-runtime"
    if MojoRuntimeAlias.MJR_USER_CONFIG_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_NAME = environ[MojoRuntimeAlias.MJR_USER_CONFIG_NAME]

    MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_FILENAME = os.path.join(
        MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_DIRECTORY,
        "{}.yaml".format(MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_NAME))

    MOJO_RUNTIME_VARIABLES.MJR_TESTROOT = None
    if MojoRuntimeAlias.MJR_TESTROOT in environ:
        MOJO_RUNTIME_VARIABLES.MJR_TESTROOT = environ[MojoRuntimeAlias.MJR_TESTROOT]

    return