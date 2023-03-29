
import unittest

class TestStartupConsole(unittest.TestCase):

    def test_startup_console(self):

        from mojo.runtime.initialize import initialize_runtime

        initialize_runtime(name="ctx", logger_name="CTX")

        from mojo.runtime.activation import console

        return

if __name__ == '__main__':
    unittest.main()
