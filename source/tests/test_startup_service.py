
import unittest

class TestStartupService(unittest.TestCase):

    def test_startup_service(self):

        from mojo.runtime.initialize import initialize_contextualize

        initialize_contextualize(name="ctx", logger_name="CTX", service_name="SomeService")

        from mojo.runtime.activation import service

        return

if __name__ == '__main__':
    unittest.main()
