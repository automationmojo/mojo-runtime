__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import List

from datetime import datetime

from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton


from mojo.runtime.variables import MOJO_RUNTIME_VARIABLES
from mojo.runtime.initialize import MOJO_RUNTIME_OVERRIDES


ctx = ContextSingleton()


def override_build_release(release: str):
    """
        This override function provides a mechanism overriding the MJR_BUILD_BRANCH
        variable and context configuration setting.

        :param release: The name of the release associated with a build.
    """
    ctx.insert(ContextPaths.BUILD_RELEASE, release)
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_RELEASE = release
    return

def override_build_branch(branch_name: str):
    """
        This override function provides a mechanism overriding the MJR_BUILD_BRANCH
        variable and context configuration setting.

        :param branch: The name of the branch the build came from.
    """
    ctx.insert(ContextPaths.BUILD_BRANCH, branch_name)
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_BRANCH = branch_name
    return

def override_build_flavor(build_flavor: str):
    """
        This override function provides a mechanism overriding the MJR_BUILD_FLAVOR
        variable and context configuration setting.

        :param build_flavor: The flavor of the build associated with a job.
    """
    ctx.insert(ContextPaths.BUILD_FLAVOR, build_flavor)
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_FLAVOR = build_flavor
    return

def override_build_name(build_name: str):
    """
        This override function provides a mechanism overriding the MJR_BUILD_NAME
        variable and context configuration setting.

        :param build_name: The build version of the build.
    """
    ctx.insert(ContextPaths.BUILD_NAME, build_name)
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_NAME = build_name
    return

def override_build_url(build_url: str):
    """
        This override function provides a mechanism overriding the MJR_BUILD_URL
        variable and context configuration setting.

        :param build_url: The url associated with the build.
    """
    ctx.insert(ContextPaths.BUILD_URL, build_url)
    MOJO_RUNTIME_VARIABLES.MJR_BUILD_URL = build_url
    return

def override_config_credentials_names(credential_names: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_CREDENTIALS_NAMES
        variable and context configuration setting.

        :param landscape_names: The names of the credential configs to use when creating the credential config.
    """
    ctx.insert(ContextPaths.CONFIG_CREDENTIALS_NAMES, credential_names)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIALS_NAMES = credential_names
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS = True
    return

def override_config_credentials_sources(sources: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_CREDENTIALS_SOURCES
        variable and context configuration setting.

        :param sources: The uri(s) of to use as the credential config search uri(s).

        ..note: If this override method is used, you must call the 'fixme' method in order
                to re-resolve the list of landscape files.
    """
    ctx.insert(ContextPaths.CONFIG_CREDENTIAL_SOURCES, sources)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_CREDENTIAL_SOURCES = sources
    return

def override_config_landscape_names(landscape_names: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_LANDSCAPE_NAMES
        variable and context configuration setting.

        :param landscape_names: The names of the landscape configs to use when creating the landscape config.
    """
    ctx.insert(ContextPaths.CONFIG_LANDSCAPE_NAMES, landscape_names)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES = landscape_names
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE = True
    return

def override_config_landscape_sources(sources: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_LANDSCAPE_SOURCES
        variable and context configuration setting.

        :param sources: The uri(s) of to use as the landscape config search uri(s).

        ..note: If this override method is used, you must call the 'fixme' method in order
                to re-resolve the list of landscape files.
    """
    ctx.insert(ContextPaths.CONFIG_LANDSCAPE_SOURCES, sources)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_LANDSCAPE_SOURCES = sources
    return

def override_config_runtime_names(runtime_names: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_RUNTIME_NAMES
        variable and context configuration setting.

        :param runtime_names: The names of the runtime files to use when selecting runtime files.

        ..note: If this override method is used, you must call the 'fixme' method in order
                to re-resolve the list of landscape files.
    """
    ctx.insert(ContextPaths.CONFIG_RUNTIME_NAMES, runtime_names)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_NAMES = runtime_names
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_RUNTIME = True
    return

def override_config_runtime_sources(sources: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_RUNTIME_SOURCES
        variable and context configuration setting.

        :param sources: The uri(s) of to use as the runtime config search uri(s).

        ..note: If this override method is used, you must call the 'fixme' method in order
                to re-resolve the list of runtime files.
    """
    ctx.insert(ContextPaths.CONFIG_RUNTIME_SOURCES, sources)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_RUNTIME_SOURCES = sources
    return

def override_config_topology_names(topology_names: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_TOPOLOGY_NAMES
        variable and context configuration setting.

        :param topology_names: The names of the topology files to use when selecting topology files.

        ..note: If this override method is used, you must call the 'fixme' method in order
                to re-resolve the list of landscape files.
    """
    ctx.insert(ContextPaths.CONFIG_TOPOLOGY_NAMES, topology_names)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES = topology_names
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY = True
    return

def override_config_topology_sources(sources: List[str]):
    """
        This override function provides a mechanism overriding the MJR_CONFIG_TOPOLOGY_SOURCES
        variable and context configuration setting.

        :param sources: The uri(s) of to use as the topology config search uri(s).

        ..note: If this override method is used, you must call the 'fixme' method in order
                to re-resolve the list of topology files.
    """
    ctx.insert(ContextPaths.CONFIG_TOPOLOGY_SOURCES, sources)
    MOJO_RUNTIME_VARIABLES.MJR_CONFIG_TOPOLOGY_SOURCES = sources
    return

def override_configuration_requirements(require_credentials: bool,
        require_landscape: bool, require_runtime: bool, require_topology: bool):
    """
        Called before or after activating the runtime in order to modify the required configuration
        files based on the applicaiton or run requirements.

        :param require_credentials: Indicates a credentials configuration file is required.
        :param require_landscape: Indicates a landscape configuration file is required.
        :param require_runtime: Indicates a runtime configuration file is required.
        :param require_topology: Indicates a topology configuration file is required.
    """
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS = require_credentials
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE = require_landscape
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_RUNTIME = require_runtime
    MOJO_RUNTIME_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY = require_topology

    return

def override_debug_breakpoints(breakpoints: List[str]):
    """
        This override function provides a mechanism overriding the MJR_BREAKPOINTS
        variable and context configuration setting.

        :param breakpoints: A list of wellknown breakpoints that have been activated.
    """
    ctx.insert(ContextPaths.DEBUG_BREAKPOINTS, breakpoints)
    MOJO_RUNTIME_VARIABLES.MJR_DEBUG_BREAKPOINTS = breakpoints
    return

def override_debug_debugger(debugger: str):
    """
        This override function provides a mechanism overriding the MJR_DEBUGGER
        variable and context configuration setting.

        :param debugger: The name of the debugger to setup.
    """
    ctx.insert(ContextPaths.DEBUG_DEBUGGER, debugger)
    MOJO_RUNTIME_VARIABLES.MJR_DEBUG_DEBUGGER = debugger
    return

def override_loglevel_console(level: str):
    """
        This override function provides a mechanism overriding the MJR_LOG_LEVEL_CONSOLE
        variable and context configuration setting.

        :param level: The console logging level.
    """
    ctx.insert(ContextPaths.LOGGING_LEVEL_CONSOLE, level)
    MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_CONSOLE = level
    return

def override_loglevel_file(level: str):
    """
        This override function provides a mechanism overriding the MJR_LOG_LEVEL_FILE
        variable and context configuration setting.

        :param level: The file log level.
    """
    ctx.insert(ContextPaths.LOGGING_LEVEL_LOGFILE, level)
    MOJO_RUNTIME_VARIABLES.MJR_LOG_LEVEL_FILE = level
    return

def override_job_id(job_id: str):
    """
        This override function provides a mechanism overriding the MJR_JOB_ID
        variable and context configuration setting.

        :param runid: A uuid string that represents the instance of this automation run.
    """
    ctx.insert(ContextPaths.JOB_ID, job_id)
    MOJO_RUNTIME_VARIABLES.MJR_JOB_ID = job_id
    return

def override_job_initiator(job_initiator: str):
    """
        This override function provides a mechanism overriding the MJR_JOB_INITIATOR
        variable and context configuration setting.

        :param job_initiator: The name of the initiator of the job.
    """

    ctx.insert(ContextPaths.JOB_INITIATOR, job_initiator)
    MOJO_RUNTIME_VARIABLES.MJR_JOB_INITIATOR = job_initiator

    return

def override_job_label(job_label: str):
    """
        This override function provides a mechanism overriding the MJR_JOB_LABEL
        variable and context configuration setting.

        :param job_label: The name of the label if any the job was run under.
    """

    ctx.insert(ContextPaths.JOB_LABEL, job_label)
    MOJO_RUNTIME_VARIABLES.MJR_JOB_LABEL = job_label

    return

def override_job_name(job_name: str):
    """
        This override function provides a mechanism overriding the MJR_JOB_NAME
        variable and context configuration setting.

        :param job_name: The name of the job.
    """

    ctx.insert(ContextPaths.JOB_NAME, job_name)
    MOJO_RUNTIME_VARIABLES.MJR_JOB_NAME = job_name

    return


def override_job_owner(job_owner: str):
    """
        This override function provides a mechanism overriding the MJR_JOB_OWNER
        variable and context configuration setting.

        :param job_owner: The name of the owner of the job.
    """

    ctx.insert(ContextPaths.JOB_OWNER, job_owner)
    MOJO_RUNTIME_VARIABLES.MJR_JOB_OWNER = job_owner

    return

def override_output_directory(output_directory: str):
    """
        This override function provides a mechanism overriding the MJR_STARTTIME
        variable and context configuration setting.

        :param output_directory: The base directory that all output artifacts will be written under.
    """
    ctx.insert(ContextPaths.OUTPUT_DIRECTORY, output_directory)
    MOJO_RUNTIME_VARIABLES.MJR_OUTPUT_DIRECTORY = output_directory
    return

def override_pipeline_id(pipeline_id: str):
    """
        This override function provides a mechanism overriding the MJR_PIPELINE_ID
        variable and context configuration setting.

        :param pipeline_id: A uuid string that represents a unique pipeline.
    """
    ctx.insert(ContextPaths.PIPELINE_ID, pipeline_id)
    MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_ID = pipeline_id
    return

def override_pipeline_name(pipeline_name: str):
    """
        This override function provides a mechanism overriding the MJR_PIPELINE_NAME
        variable and context configuration setting.

        :param pipeline_name: A string that contains the name for a given pipeline.
    """
    ctx.insert(ContextPaths.PIPELINE_NAME, pipeline_name)
    MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_NAME = pipeline_name
    return

def override_pipeline_name(pipeline_instance: str):
    """
        This override function provides a mechanism overriding the MJR_PIPELINE_NAME
        variable and context configuration setting.

        :param pipeline_instance: A uuid string that represents the instance of a given pipeline.
    """
    ctx.insert(ContextPaths.PIPELINE_INSTANCE, pipeline_instance)
    MOJO_RUNTIME_VARIABLES.MJR_PIPELINE_INSTANCE = pipeline_instance
    return

def override_run_id(run_id: str):
    """
        This override function provides a mechanism overriding the MJR_RUN_ID
        variable and context configuration setting.

        :param runid: A uuid string that represents the instance of this automation run.
    """
    ctx.insert(ContextPaths.RUNID, run_id)
    MOJO_RUNTIME_VARIABLES.MJR_RUN_ID = run_id
    return

def override_starttime(starttime: datetime):
    """
        This override function provides a mechanism overriding the MJR_STARTTIME
        variable and context configuration setting.

        :param starttime: The date and time to set as the starttime of this run.
    """
    ctx.insert(ContextPaths.STARTTIME, starttime)
    MOJO_RUNTIME_VARIABLES.MJR_STARTTIME = starttime
    return

def override_testroot(testroot: str):
    """
        This override function provides a mechanism overriding the MJR_TESTROOT
        variable and context configuration setting.

        :param testroot: The full path of the root of the tests folder.
    """
    MOJO_RUNTIME_VARIABLES.MJR_TESTROOT = testroot
    ctx.insert(ContextPaths.TESTROOT, testroot)
    return
