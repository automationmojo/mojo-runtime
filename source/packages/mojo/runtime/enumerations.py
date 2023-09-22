
from enum import Enum

class ActivationProfile(str, Enum):
    Command = "command"
    Console = "console"
    Orchestration = "orchestration"
    Service = "service"
    TestRun = "testrun"

class JobType(str, Enum):
    Unknown = "unknown"
    Console = "console"
    Service = "service"
    TestRun = "testrun"
    Orchestration = "orchestration"
