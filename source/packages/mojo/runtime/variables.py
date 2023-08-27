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

from typing import List, Optional


import os

from datetime import datetime
from enum import Enum
from uuid import uuid4

from mojo.collections.context import ContextPaths
from mojo.collections.wellknown import ContextSingleton

from mojo.config.variables import MOJO_CONFIG_VARIABLES, resolve_configuration_variables

from mojo.xmods.xdatetime import (
    parse_datetime, DATETIME_FORMAT_FILESYSTEM, DATETIME_FORMAT_TIMESTAMP
)
from mojo.xmods.xlogging.levels import LogLevel

from mojo.runtime.initialize import MOJO_RUNTIME_OVERRIDES, MojoRuntimeAlias


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


class MOJO_RUNTIME_VARIABLES(MOJO_CONFIG_VARIABLES):
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    MJR_SERVICE_NAME = MOJO_RUNTIME_OVERRIDES.MJR_SERVICE_NAME
    MJR_LOGGER_NAME = MOJO_RUNTIME_OVERRIDES.MJR_LOGGER_NAME

    MJR_OUTPUT_DIRECTORY = None

    MJR_ACTIVATION_PROFILE = None

    MJR_AUTOMATION_POD = DefaultValue.NotSet

    MJR_BUILD_RELEASE = DefaultValue.NotSet
    MJR_BUILD_BRANCH = DefaultValue.NotSet
    MJR_BUILD_FLAVOR = DefaultValue.NotSet
    MJR_BUILD_NAME = DefaultValue.NotSet
    MJR_BUILD_URL = DefaultValue.NotSet

    MJR_DEBUG_BREAKPOINTS = None
    MJR_DEBUG_DEBUGGER = None

    MJR_EXTENSION_FACTORY_ADDITIONS = None

    MJR_INTERACTIVE_CONSOLE = False

    MJR_RUN_ID = DefaultValue.NotSet

    MJR_PIPELINE_ID = DefaultValue.NotSet
    MJR_PIPELINE_NAME = DefaultValue.NotSet
    MJR_PIPELINE_INSTANCE = DefaultValue.NotSet

    MJR_JOB_ID = DefaultValue.NotSet
    MJR_JOB_TYPE = JobType.Unknown.value
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


def resolve_runtime_variables():

    environ = os.environ

    resolve_configuration_variables()

    ctx = ContextSingleton()

    if MojoRuntimeAlias.MJR_STARTTIME in environ:
        passedVal = environ[MojoRuntimeAlias.MJR_STARTTIME]
        starttime = None
        if passedVal.find(":") > -1:
            starttime = parse_datetime(passedVal, DATETIME_FORMAT_TIMESTAMP)
        else:
            starttime = parse_datetime(passedVal, DATETIME_FORMAT_FILESYSTEM)
        MOJO_RUNTIME_VARIABLES.MJR_STARTTIME = starttime

    MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = None
    if MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY in environ:
        MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = environ[MojoRuntimeAlias.MJR_OUTPUT_DIRECTORY]

    MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = None
    if MojoRuntimeAlias.MJR_ACTIVATION_PROFILE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = environ[MojoRuntimeAlias.MJR_ACTIVATION_PROFILE]

    MOJO_RUNTIME_VARIABLES.MJR_AUTOMATION_POD = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_AUTOMATION_POD in environ:
        MOJO_RUNTIME_VARIABLES.MJR_AUTOMATION_POD = environ[MojoRuntimeAlias.MJR_AUTOMATION_POD]


    MOJO_RUNTIME_VARIABLES.MJR_BUILD_RELEASE = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_RELEASE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_RELEASE = environ[MojoRuntimeAlias.MJR_BUILD_RELEASE]
    ctx.insert(ContextPaths.BUILD_RELEASE, MOJO_RUNTIME_VARIABLES.MJR_BUILD_RELEASE)

    MOJO_RUNTIME_VARIABLES.MJR_BUILD_BRANCH = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_BRANCH in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_BRANCH = environ[MojoRuntimeAlias.MJR_BUILD_BRANCH]
    ctx.insert(ContextPaths.BUILD_BRANCH, MOJO_RUNTIME_VARIABLES.MJR_BUILD_BRANCH)

    MOJO_RUNTIME_VARIABLES.MJR_BUILD_NAME = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_NAME = environ[MojoRuntimeAlias.MJR_BUILD_NAME]
    ctx.insert(ContextPaths.BUILD_NAME, MOJO_RUNTIME_VARIABLES.MJR_BUILD_NAME)

    MOJO_RUNTIME_VARIABLES.MJR_BUILD_FLAVOR = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_FLAVOR in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_FLAVOR = environ[MojoRuntimeAlias.MJR_BUILD_FLAVOR]
    ctx.insert(ContextPaths.BUILD_FLAVOR, MOJO_RUNTIME_VARIABLES.MJR_BUILD_FLAVOR)

    MOJO_RUNTIME_VARIABLES.MJR_BUILD_URL = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_BUILD_URL in environ:
        MOJO_RUNTIME_VARIABLES.MJR_BUILD_URL = environ[MojoRuntimeAlias.MJR_BUILD_URL]
    ctx.insert(ContextPaths.BUILD_URL, MOJO_RUNTIME_VARIABLES.MJR_BUILD_URL)


    MOJO_RUNTIME_VARIABLES.MJR_DEBUG_BREAKPOINTS = None
    if MojoRuntimeAlias.MJR_DEBUG_BREAKPOINTS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_DEBUG_BREAKPOINTS = environ[MojoRuntimeAlias.MJR_DEBUG_BREAKPOINTS]

    MOJO_RUNTIME_VARIABLES.MJR_DEBUG_DEBUGGER = None
    if MojoRuntimeAlias.MJR_DEBUG_DEBUGGER in environ:
        MOJO_RUNTIME_VARIABLES.MJR_DEBUG_DEBUGGER = environ[MojoRuntimeAlias.MJR_DEBUG_DEBUGGER]

    MOJO_RUNTIME_VARIABLES.MJR_EXTENSION_FACTORY_ADDITIONS = None
    if MojoRuntimeAlias.MJR_EXTENSION_FACTORY_ADDITIONS in environ:
        MOJO_RUNTIME_VARIABLES.MJR_EXTENSION_FACTORY_ADDITIONS = environ[MojoRuntimeAlias.MJR_EXTENSION_FACTORY_ADDITIONS]


    MOJO_RUNTIME_VARIABLES.MJR_RUN_ID = str(uuid4())
    if MojoRuntimeAlias.MJR_RUN_ID in environ:
        MOJO_RUNTIME_VARIABLES.MJR_RUN_ID = environ[MojoRuntimeAlias.MJR_RUN_ID]
    ctx.insert(ContextPaths.RUNID, MOJO_RUNTIME_VARIABLES.MJR_RUN_ID)


    MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_ID = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_PIPELINE_ID in environ:
        MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_ID = environ[MojoRuntimeAlias.MJR_PIPELINE_ID]
    ctx.insert(ContextPaths.PIPELINE_ID, MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_ID)
    
    MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_NAME = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_PIPELINE_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_NAME = environ[MojoRuntimeAlias.MJR_PIPELINE_NAME]
    ctx.insert(ContextPaths.PIPELINE_NAME, MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_NAME)

    MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_INSTANCE = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_PIPELINE_INSTANCE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_INSTANCE = environ[MojoRuntimeAlias.MJR_PIPELINE_INSTANCE]
    ctx.insert(ContextPaths.PIPELINE_INSTANCE, MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_INSTANCE)


    MOJO_RUNTIME_VARIABLES.MJR_JOB_ID = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_ID in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_ID = environ[MojoRuntimeAlias.MJR_JOB_ID]
    ctx.insert(ContextPaths.JOB_ID, MOJO_RUNTIME_VARIABLES.MJR_JOB_ID)

    MOJO_RUNTIME_VARIABLES.MJR_JOB_INITIATOR = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_INITIATOR in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_INITIATOR = environ[MojoRuntimeAlias.MJR_JOB_INITIATOR]
    ctx.insert(ContextPaths.JOB_INITIATOR, MOJO_RUNTIME_VARIABLES.MJR_JOB_INITIATOR)

    MOJO_RUNTIME_VARIABLES.MJR_JOB_LABEL = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_LABEL in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_LABEL = environ[MojoRuntimeAlias.MJR_JOB_LABEL]
    ctx.insert(ContextPaths.JOB_LABEL, MOJO_RUNTIME_VARIABLES.MJR_JOB_LABEL)

    MOJO_RUNTIME_VARIABLES.MJR_JOB_NAME = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_NAME in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_NAME = environ[MojoRuntimeAlias.MJR_JOB_NAME]
    ctx.insert(ContextPaths.JOB_NAME, MOJO_RUNTIME_VARIABLES.MJR_JOB_NAME)

    MOJO_RUNTIME_VARIABLES.MJR_JOB_OWNER = DefaultValue.NotSet
    if MojoRuntimeAlias.MJR_JOB_OWNER in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_OWNER = environ[MojoRuntimeAlias.MJR_JOB_OWNER]
    ctx.insert(ContextPaths.JOB_OWNER, MOJO_RUNTIME_VARIABLES.MJR_JOB_OWNER)

    MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Unknown.value
    if MojoRuntimeAlias.MJR_JOB_TYPE in environ:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = environ[MojoRuntimeAlias.MJR_JOB_TYPE]
    ctx.insert(ContextPaths.JOB_TYPE, MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE)


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


    MOJO_RUNTIME_VARIABLES.MJR_TESTROOT = None
    if MojoRuntimeAlias.MJR_TESTROOT in environ:
        MOJO_RUNTIME_VARIABLES.MJR_TESTROOT = environ[MojoRuntimeAlias.MJR_TESTROOT]

    return