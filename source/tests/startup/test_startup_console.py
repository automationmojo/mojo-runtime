
import unittest

class TestStartupConsole(unittest.TestCase):

    def test_startup_console_output_path(self):

        from mojo.runtime.initialize import initialize_runtime

        initialize_runtime(name="mjr", logger_name="MJR")

        import mojo.runtime.activation.console

        from mojo.runtime.paths import get_path_for_output

        output_directory = get_path_for_output()

        assert output_directory.startswith("/tmp")

        return

if __name__ == '__main__':
    unittest.main()
