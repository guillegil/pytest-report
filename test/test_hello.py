
import pytest
import pytest_report

from pytest_report import log


@pytest.fixture
def setup():
    log.info('This is info from setup')
    log.warning('This is warning from setup')
    yield None

@pytest.mark.parametrize(
        "arg1,arg2",
        [
            (1,2),
            (3,4),
            (5,6),
        ]
)
def test_parameters(arg1, arg2):
    log.info(f'Parameters are {arg1=} {arg2=}')

def test_procedure(setup):
    log.step("Initialize environment and load test configuration")      # 1.
    log.substep("Load environment variables from config file")          # 1.1
    log.substep("Validate mandatory configuration keys are present")    # 1.2
    log.substep("Establish initial database connection")                # 1.3

    log.step("Start the core application service")                      # 2.
    log.substep("Launch background worker process")                     # 2.1
    log.substep("Verify service is listening on expected port")         # 2.2
    log.substep("Check that startup logs contain no errors")            # 2.3

    log.step("Execute main workflow scenario")                          # 3.
    log.substep("Send mock API request with valid payload")             # 3.1
    log.substep("Validate system’s response matches schema")            # 3.2
    log.substep("Confirm record was written into database")             # 3.3
    log.substep("Trigger downstream notification handler")              # 3.4

    log.step("Test error handling paths")                               # 4.
    log.substep("Send malformed API request to trigger 400 error")      # 4.1
    log.substep("Confirm error response contains proper message")       # 4.2
    log.substep("Inject artificial DB outage and retry workflow")       # 4.3
    log.substep("Ensure system gracefully recovers when DB is restored")# 4.4

    log.step("Clean up and teardown environment")                       # 5.
    log.substep("Terminate background worker process")                  # 5.1
    log.substep("Drop temporary test database tables")                  # 5.2
    log.substep("Remove test configuration files")                      # 5.3
    log.substep("Release memory and close all connections")             # 5.4

def test_error():
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')

    print("This is gonna break everything")
    