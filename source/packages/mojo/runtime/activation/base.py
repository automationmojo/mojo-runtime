"""
.. module:: activate
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by test files to ensure the test environment is initialized in
               the correct order.

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
import sys
import uuid

from mojo.errors.exceptions import (
    ConfigurationError,
    SemanticError
)
from mojo.errors.xtraceback import (
    TRACEBACK_CONFIG,
    VALID_MEMBER_TRACE_POLICY,
)

from mojo.runtime.initialize import MOJO_RUNTIME_OVERRIDES

# Perform a sematic check to see who is importing the akit.activation.base module.  We
# need to make sure that the user is following the proper semantics and importing an activation
# profile and not directly importing this module.  This will enforce the setting of the
# activation profile in the global variables and enforce a proper environment activation
# sequence is followed.
importer_frame = sys._getframe()
while True:
    importer_frame = importer_frame.f_back
    if importer_frame.f_code.co_filename.find("importlib") < 0:
        break
if "__activation_profile__" not in importer_frame.f_locals:
    errmsg = "The 'mojo.runtime.activation.base' should not be directly imported." \
             "  The environment activation should always happen by importing" \
             " an activation profile module."
    raise SemanticError(errmsg)

# Perform a semantic check to make sure that the `contextualize.overrides` module has been loaded
# before this module has been imported and that it was properly initiaized.  This is crucial so
# we have the correct context name and a logger name.
if "mojo.runtime.initialize" not in sys.modules:
    errmsg = "The 'mojo.runtime.activation.base' should not be imported unless the " \
             "`initialize_runtime` module has been called to set the global name " \
             "of the application context."
    raise SemanticError(errmsg)
elif MOJO_RUNTIME_OVERRIDES.MJR_NAME is None:
    errmsg = "The `initialize_runtime` method must be called to set the context" \
             "name and logger name before attempting to activate the runtime."
    raise SemanticError(errmsg)

# =======================================================================================
# The way we start up the test framework and the order which things come up in is a very
# important part of the automation process.  It effects whether or not logging is brought
# up consistently before all modules start using it.  It ensures that no matter how we
# enter into an automation process, whether via a test runner, terminal, or debugging a single
# file that we properly parse arguments and settings and launch the automation process
# consistently.
#
# Because of these necessities, we setup the activate module so it is the first thing
# scripts and tests files that consume the test framework will import to ensure the
# startup process is always consistent
#
# The framework has a special activation module :module:`akit.environment.console` that is
# used when bringing up the test framework in a console.  This special method redirects

# Activation Step - 1: Force the global shared context to load, we want this to happen as early
# as possible because we don't want to every replace its reference or invalidate
# any references to it that someone might have acquired.
from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton # pylint: disable=wrong-import-position

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

DEFAULT_PATH_EXPANSIONS = [
    os.path.expanduser,
    os.path.expandvars,
    os.path.abspath
]
def expand_path(path_in, expansions=DEFAULT_PATH_EXPANSIONS):

    path_out = path_in
    for expansion_func in expansions:
        path_out = expansion_func(path_out)

    return path_out

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
# determines where logging will go and is different depending on the activation mode of the test framework
if MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY is not None:
    outdir_full = expand_path(MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY % fill_dict)
else:
    if jobtype == JobType.Console:
        default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "console", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_CONSOLE, default=default_dir_template)
        filled_dir_results = outdir_template % fill_dict
        outdir_full = expand_path(filled_dir_results)
        ctx.insert(ContextPaths.RESULT_PATH_FOR_CONSOLE, outdir_full)

    elif jobtype == JobType.Orchestration:
        default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "orchestration", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_ORCHESTRATION, default=default_dir_template)
        filled_dir_results = outdir_template % fill_dict
        outdir_full = expand_path(filled_dir_results)
        ctx.insert(ContextPaths.RESULT_PATH_FOR_ORCHESTRATION, outdir_full)

    elif jobtype == JobType.Service:
        default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "service", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_SERVICES, default=default_dir_template)
        filled_dir_results = outdir_template % fill_dict
        outdir_full = expand_path(filled_dir_results)
        ctx.insert(ContextPaths.RESULT_PATH_FOR_SERVICES, outdir_full)

    else:
        default_dir_template = os.path.join(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "results", "testresults", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_TESTS, default=default_dir_template)
        filled_dir_results = outdir_template % fill_dict
        outdir_full = expand_path(filled_dir_results)
        ctx.insert(ContextPaths.RESULT_PATH_FOR_TESTS, outdir_full)

ctx.insert(ContextPaths.OUTPUT_DIRECTORY, outdir_full)

# Activation Step - 7: Import the logging module so we can be the trigger the logging configuration
# for standard out
import mojo.xmods.xlogging.foundations # pylint: disable=unused-import,wrong-import-position
