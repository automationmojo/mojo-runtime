
import unittest

class TestStartupConsole(unittest.TestCase):

    def test_startup_console(self):

        from contextualize.initialize import initialize_contextualize

        initialize_contextualize(name="ctx", logger_name="CTX")

        from contextualize.activation import console

        return

if __name__ == '__main__':
    unittest.main()
