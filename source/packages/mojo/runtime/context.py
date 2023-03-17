"""
.. module:: context
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`Context` object and :class:`ContextCursor` that
               are used to maintain the shared automation context.

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


from typing import Any, List, Optional

from mojo.xmods.xcollections.context import Context

from mojo.runtime.configuration import CONFIGURATION_MAP


# Initialize the global context
context = Context()
context.insert("/configuration", CONFIGURATION_MAP)
context.insert("/environment", {})

