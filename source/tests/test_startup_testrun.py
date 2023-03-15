
import unittest

class TestStartupTestRun(unittest.TestCase):

    def test_startup_testrun(self):

        from contextualize.initialize import initialize_contextualize

        initialize_contextualize(name="ctx", logger_name="CTX")

        from contextualize.activation import testrun

        return

if __name__ == '__main__':
    unittest.main()
