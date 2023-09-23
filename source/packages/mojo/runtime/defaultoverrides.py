"""
.. module:: defaultoverrides
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains defaults that can be overridden to customize the runtime.

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

from mojo.config.overrides import MOJO_CONFIG_OVERRIDES

class MOJO_RUNTIME_OVERRIDES(MOJO_CONFIG_OVERRIDES):

    MJR_LOGGER_NAME = "MJR"
    MJR_SERVICE_NAME = None
