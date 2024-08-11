
import unittest

import os

from mojo.xmods.xdatetime import parse_datetime, DATETIME_FORMAT_FILESYSTEM

class TestStartupTestRun(unittest.TestCase):

    def test_startup_testrun(self):

        from mojo.runtime.initialize import initialize_runtime

        initialize_runtime(name="mjr", logger_name="MJR")

        from mojo.runtime.activation import activate_runtime, ActivationProfile
        activate_runtime(profile=ActivationProfile.TestRun)

        from mojo.runtime.runtimevariables import MOJO_RUNTIME_VARIABLES
        from mojo.runtime.paths import get_path_for_output

        output_directory = get_path_for_output()

        assert output_directory.startswith(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY), \
            "The output path should reside under the home directory"

        output_directory = output_directory.replace(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "").lstrip(os.sep)
        other_parts = output_directory.split(os.sep)

        assert other_parts[0] == "results", "Next directory should have been 'results'."
        assert other_parts[1] == "testresults", "Next directory should have been 'testresults'."

        dtcomp = parse_datetime(other_parts[2], datetime_format=DATETIME_FORMAT_FILESYSTEM)

        return

if __name__ == '__main__':
    unittest.main()
