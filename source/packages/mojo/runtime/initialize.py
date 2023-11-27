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

from typing import Optional

import os

from mojo.config.overrides import MOJO_CONFIG_OVERRIDES

from mojo.runtime.defaultoverrides import MOJO_RUNTIME_OVERRIDES


class MOJO_RUNTIME_STATE:
    INITIALIZED = False


def initialize_runtime(*, name: Optional[str]=None,
                          home_dir: Optional[str]=None,
                          logger_name: Optional[str]=None,
                          default_configuration: dict=None,
                          service_name: Optional[str]=None):

    # =======================================================================================
    # The way we start up the test framework and the order which things come up in is a very
    # important part of the automation process.  It effects whether or not logging is brought
    # up consistently before all modules start using it.  It ensures that no matter how we
    # enter into an automation process, whether via a test runner, terminal, or debugging a single
    # file that we properly parse arguments and settings and launch the automation process
    # consistently.
    

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

    # The runtime variables can tell us where to find extensions, so we must resolve the runtime
    # varaibles before attempting to resolve any extension factories.
    resolve_runtime_variables()

    return
