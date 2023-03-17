
import unittest

class TestStartupTestRun(unittest.TestCase):

    def test_startup_testrun(self):

        from mojo.runtime.initialize import initialize_contextualize

        initialize_contextualize(name="ctx", logger_name="CTX")

        from mojo.runtime.activation import testrun

        return

if __name__ == '__main__':
    unittest.main()
