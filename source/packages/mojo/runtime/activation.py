"""
.. module:: activation
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains methods that implement the activation process.

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

from typing import Optional

import os
import tempfile
import uuid

from logging import FileHandler
from logging.handlers import RotatingFileHandler


from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton # pylint: disable=wrong-import-position


from mojo.errors.exceptions import ConfigurationError, SemanticError
from mojo.errors.xtraceback import (
    TRACEBACK_CONFIG,
    VALID_MEMBER_TRACE_POLICY,
)


from mojo.runtime.enumerations import ActivationProfile, JobType
from mojo.runtime.variablenames import MOJO_RUNTIME_VARNAMES

from mojo.runtime.variables import MOJO_RUNTIME_VARIABLES

from mojo.xmods.xlogging.levels import LogLevel

def activate_profile_command():

    # Guard against attemps to activate more than one, activation profile.
    if MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE
        )
        raise SemanticError(errmsg)

    MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = ActivationProfile.Command
    MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Unknown.value
    os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE

    temp_output_dir = tempfile.mkdtemp()
    MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = temp_output_dir

    activate_profile_common()

    from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

    LoggingDefaults.DefaultFileLoggingHandler = FileHandler
    logging_initialize()


    return

def activate_profile_console():

    # Guard against attemps to activate more than one, activation profile.
    if MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE
        )
        raise SemanticError(errmsg)

    MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = ActivationProfile.Console
    MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.Console.value
    os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE

    temp_output_dir = tempfile.mkdtemp()
    MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = temp_output_dir

    def showlog():

        print("OUTPUT FOLDER: {}".format(MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY))
        print("")

        return

    if MOJO_RUNTIME_VARIABLES.MJR_INTERACTIVE_CONSOLE:
        # If we are running in an interactive console, then we need to reduce the
        # console log level and we need to output log data to a console log file.

        # Only set the log levels if they were not previously set.  An option to a base
        # command may have set this in order to turn on a different level of verbosity
        if MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE is None:
            MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE = LogLevel.QUIET

        # For console activation we don't want to log to the console and we want
        # to point the logs to a different output folder
        os.environ[MOJO_RUNTIME_VARNAMES.MJR_LOG_LEVEL_CONSOLE] = str(MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE)
        os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE
        os.environ[MOJO_RUNTIME_VARNAMES.MJR_OUTPUT_DIRECTORY] = str(MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY)

        activate_profile_common()

        from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

        LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
        logging_initialize()

        showlog()

    else:

        activate_profile_common()

        from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

        LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
        logging_initialize()

    return

def activate_profile_service():

    # Guard against attempts to activate more than one, activation profile.
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

    activate_profile_common()

    from mojo.xmods.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

    LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler

    logging_initialize()


    return

def activate_profile_testrun():

    # Guard against attemps to activate more than one, activation profile.
    if MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE
        )
        raise RuntimeError(errmsg)

    MOJO_RUNTIME_VARIABLES.MJR_ACTIVATION_PROFILE = ActivationProfile.TestRun
    MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE = LogLevel.WARNING

    MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE = JobType.TestRun.value

    os.environ[MOJO_RUNTIME_VARNAMES.MJR_LOG_LEVEL_CONSOLE] = str(MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE)
    os.environ[MOJO_RUNTIME_VARNAMES.MJR_JOB_TYPE] = str(MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE)

    activate_profile_common()

    ctx = ContextSingleton()
    ctx.insert(ContextPaths.RESULT_PATH_FOR_TESTS,  MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY)

    from mojo.xmods.xlogging.foundations import logging_initialize
    
    logging_initialize()

    return

def activate_profile_common():

    # =======================================================================================
    # The way we start up the test framework and the order which things come up in is a very
    # important part of the automation process.  It effects whether or not logging is brought
    # up consistently before all modules start using it.  It ensures that no matter how we
    # enter into an automation process, whether via a test runner, terminal, or debugging a single
    # file that we properly parse arguments and settings and launch the automation process
    # consistently.
    
    ctx = ContextSingleton()

    from mojo.xmods.xlogging.levels import LOG_LEVEL_NAMES
    from mojo.xmods.xdatetime import DATETIME_FORMAT_FILESYSTEM

    # Activation Step - 3: Process the environment variable overrides for any of the AKIT configuration
    # variables. This needs to happen before we load or create an initial user configuration
    # because the variables may effect the values we write into the user configuration file.
    from mojo.runtime.variables import (
        MOJO_RUNTIME_VARIABLES,
        DefaultValue,
        JobType
    )

    # We set all the variables for config file options from the environment
    # we just loaded, these might get overridden late but that is ok
    current_traceback_policy = ctx.lookup(ContextPaths.DIAGNOSTICS_TRACEBACK_POLICY_OVERRIDE, default=None)
    if current_traceback_policy is None and TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE is not None:
        if TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE in VALID_MEMBER_TRACE_POLICY:
            ctx.insert(ContextPaths.DIAGNOSTICS_TRACEBACK_POLICY_OVERRIDE, TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE)
        else:
            errmsg = "Invalid traceback policy environment value. TRACEBACK_POLICY_OVERRIDE={}".format(
                TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE
            )
            raise ConfigurationError(errmsg)

    # Activation Step - 5: After
    if MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE is not None and MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE in LOG_LEVEL_NAMES:
        console_level = MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE
    else:
        console_level = "INFO"
        MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE = console_level

    if MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_FILE is not None and MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_FILE in LOG_LEVEL_NAMES:
        logfile_level = MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_FILE
    else:
        logfile_level = "DEBUG"
        MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_FILE = logfile_level

    ctx.insert(ContextPaths.LOGGING_LEVEL_CONSOLE, console_level)
    ctx.insert(ContextPaths.LOGGING_LEVEL_LOGFILE, logfile_level)

    jobtype = ctx.lookup(ContextPaths.JOB_TYPE, default=MOJO_RUNTIME_VARIABLES.MJR_JOB_TYPE)

    starttime_name = MOJO_RUNTIME_VARIABLES.MJR_STARTTIME.strftime(DATETIME_FORMAT_FILESYSTEM)

    fill_dict = {
        "starttime": starttime_name
    }

    if MOJO_RUNTIME_VARIABLES.MJR_JOB_ID is None or MOJO_RUNTIME_VARIABLES.MJR_JOB_ID == DefaultValue.NotSet:
        MOJO_RUNTIME_VARIABLES.MJR_JOB_ID = str(uuid.uuid4())

    # We want to pull the console and testresults value from the configuration, because if its not there it
    # will be set from the default_dir_template variable
    env = ctx.lookup("/environment")
    ctx.insert(ContextPaths.STARTTIME, MOJO_RUNTIME_VARIABLES.MJR_STARTTIME)
    ctx.insert(ContextPaths.JOB_ID, MOJO_RUNTIME_VARIABLES.MJR_JOB_ID)

    outdir_full = None

    # Figure out which output directory to set as the current process output directory.  The output directory
    # determines where loggin will go and is different depending on the activation mode of the test framework
    if MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY is None:
        filled_dir_results = None
        if jobtype == JobType.Console:
            default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "console", "%(starttime)s")
            outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_CONSOLE, default=default_dir_template)
            filled_dir_results = outdir_template % fill_dict
            ctx.insert(ContextPaths.RESULT_PATH_FOR_CONSOLE, filled_dir_results)

        elif jobtype == JobType.Orchestration:
            default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "orchestration", "%(starttime)s")
            outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_ORCHESTRATION, default=default_dir_template)
            filled_dir_results = outdir_template % fill_dict
            ctx.insert(ContextPaths.RESULT_PATH_FOR_ORCHESTRATION, filled_dir_results)

        elif jobtype == JobType.Service:
            default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "service", "%(starttime)s")
            outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_SERVICES, default=default_dir_template)
            filled_dir_results = outdir_template % fill_dict
            ctx.insert(ContextPaths.RESULT_PATH_FOR_SERVICES, filled_dir_results)

        else:
            default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "testresults", "%(starttime)s")
            outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_TESTS, default=default_dir_template)
            filled_dir_results = outdir_template % fill_dict
            ctx.insert(ContextPaths.RESULT_PATH_FOR_TESTS, filled_dir_results)

        MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = filled_dir_results

    if ctx.lookup(ContextPaths.OUTPUT_DIRECTORY) is None:
        ctx.insert(ContextPaths.OUTPUT_DIRECTORY, MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY)

    return


def activate_runtime(*, profile: Optional[ActivationProfile]=ActivationProfile.Console):

    # Activate the runtime profile specified
    if profile == ActivationProfile.Command:
        activate_profile_command()
    elif profile == ActivationProfile.Console:
        activate_profile_console()
    elif profile == ActivationProfile.Service:
        activate_profile_service()
    elif profile == ActivationProfile.TestRun:
        activate_profile_testrun()
    else:
        errmsg = f"Unknown runtime activation profile. profile={profile}"
        raise SemanticError(errmsg)

    return