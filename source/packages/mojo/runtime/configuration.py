"""
.. module:: configuration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the functions that are used to load the automation
               configuration files and overlay the settings on top of the default runtime
               configuration.

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

from typing import Any, Dict

import os
import yaml

from mojo.xmods.xcollections.mergemap import MergeMap

from mojo.runtime.initialize import MOJO_RUNTIME_OVERRIDES
from mojo.runtime.variables import MOJO_RUNTIME_VARIABLES

# The override configuration dictionary is added to the ChainMap first so it takes
# precidence over all other dictionaries in the chain.
CONFIGURATION_MAP = MergeMap(MOJO_RUNTIME_OVERRIDES.DEFAULT_CONFIGURATION)


def load_user_configuration(tryonly: bool=True) -> Dict[str, Any]:

    # We create the default configuration here because there are a couple of environment
    # variables that might modify our default configuration values, we want to delay
    # locking the values from the variables into a default configuration declaration until
    # this function is called.
    user_configuration_file = os.path.expanduser(os.path.expandvars(os.path.abspath(MOJO_RUNTIME_VARIABLES.MJR_USER_CONFIG_FILENAME)))
    if os.path.exists(user_configuration_file):
        overlay_configuration(user_configuration_file)
    elif not tryonly:
        errmsg = "The specified configuration file '{}' does not exist."
        raise FileNotFoundError(errmsg)

    return


def overlay_configuration(filename: str) -> None:

    configuration_file = os.path.expanduser(os.path.expandvars(os.path.abspath(filename)))
    if os.path.exists(configuration_file):

        with open(configuration_file, 'r') as rcf:
            rcf_content = rcf.read()
            runtime_configuration = yaml.safe_load(rcf_content)

        # To overlay a map, we always insert the map in the zero position
        CONFIGURATION_MAP.maps.insert(0, runtime_configuration)

    else:
        errmsg = "The specified configuration file '{}' does not exist."
        raise FileNotFoundError(errmsg)

    return

