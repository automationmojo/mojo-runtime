
import unittest

class TestStartupService(unittest.TestCase):

    def test_startup_service(self):

        from contextualize.initialize import initialize_contextualize

        initialize_contextualize(name="ctx", logger_name="CTX", service_name="SomeService")

        from contextualize.activation import service

        return

if __name__ == '__main__':
    unittest.main()
