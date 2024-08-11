
import unittest

class TestStartupService(unittest.TestCase):

    def test_startup_service(self):

        from mojo.runtime.initialize import initialize_runtime

        service_name = "SomeService"

        initialize_runtime(name="mjr", logger_name="MJR", service_name=service_name)

        from mojo.runtime.activation import activate_runtime, ActivationProfile
        activate_runtime(profile=ActivationProfile.Service)

        from mojo.runtime.runtimevariables import MOJO_RUNTIME_VARIABLES
        from mojo.runtime.paths import get_path_for_output

        output_directory = get_path_for_output()

        assert output_directory.startswith(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY), \
            "The output path should reside under the home directory"

        output_directory = output_directory.replace(MOJO_RUNTIME_VARIABLES.MJR_HOME_DIRECTORY, "").lstrip("/")
        other_parts = output_directory.split("/")

        assert other_parts[0] == "services", "Next directory should have been 'services'."
        assert other_parts[1] == service_name, f"Next directory should have been '{service_name}'."

        return

if __name__ == '__main__':
    unittest.main()
