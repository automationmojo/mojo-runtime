
import unittest

from mojo.xmods.xdatetime import parse_datetime

class TestStartupTestRun(unittest.TestCase):

    def test_startup_testrun(self):

        from mojo.runtime.initialize import initialize_runtime

        initialize_runtime(name="mjr", logger_name="MJR")

        import mojo.runtime.activation.testrun

        from mojo.runtime.variables import MOJO_RUNTIME_VARIABLES
        from mojo.runtime.paths import get_path_for_output

        output_directory = get_path_for_output()

        assert output_directory.startswith(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY), \
            "The output path should reside under the home directory"

        output_directory = output_directory.replace(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "").lstrip("/")
        other_parts = output_directory.split("/")

        assert other_parts[0] == "results", "Next directory should have been 'results'."
        assert other_parts[1] == "testresults", "Next directory should have been 'testresults'."

        dtcomp = parse_datetime(other_parts[2])

        return

if __name__ == '__main__':
    unittest.main()
