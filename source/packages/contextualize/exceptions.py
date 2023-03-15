"""
.. module:: exceptions
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains contextualize specific exceptions.

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

class ConfigurationError(BaseException):
    """
        The base error object for errors that indicate that there is an issue related
        to improper configuration.
    """

class InvalidConfigurationError(ConfigurationError):
    """
        This error is raised when an IntegrationCoupling object has been passed invalid configuration parameters.
    """

class MissingConfigurationError(ConfigurationError):
    """
        This error is raised when an IntegrationCoupling object is missing required configuration parameters.
    """

class SemanticError(BaseException):
    """
        The base error object for errors that indicate that there is an issue with
        a piece of automation code and with the way the Automation Kit code is being
        utilized.
    """

