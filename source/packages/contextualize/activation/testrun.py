"""
.. module:: testrun
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by test runs to activate the test environment
               for use by a test run.

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

from contextualize.variables import ActivationProfile, CONTEXTUALIZE_VARIABLES, JobType
from contextualize.initialize import ContextAlias

__activation_profile__ = ActivationProfile.TestRun

# Guard against attemps to activate more than one, activation profile.
if CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE is not None:
    errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
        CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE
    )
    raise RuntimeError(errmsg)

CONTEXTUALIZE_VARIABLES.CONTEXT_ACTIVATION_PROFILE = ActivationProfile.TestRun

CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE = JobType.TestRun

os.environ[ContextAlias.CONTEXT_JOB_TYPE] = str(CONTEXTUALIZE_VARIABLES.CONTEXT_JOB_TYPE)

import contextualize.activation.base
