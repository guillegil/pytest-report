"""
Modern pytest plugin template with clean hook implementations.
"""
import pytest
from pytest import Item, Config, Session, TestReport, CallInfo
from pathlib import Path
from typing import Optional, List, Union, Any
import warnings

from .reporter.reporter import Reporter
from pytest_meta import meta

from pytest_checker import check

class PytestReportPlugin:
    """
    A modern pytest plugin template with commonly used hooks.
    
    This plugin demonstrates best practices for:
    - Hook registration using @pytest.hookimpl
    - Proper configuration management
    - Lazy initialization
    - Clean separation of concerns
    """
    
    def __init__(self):
        self.config     : Optional[Config] = None
        self.reporter   : Reporter = None
    
    # ========== CONFIGURATION HOOKS ==========
    @pytest.hookimpl
    def pytest_configure(self, config: Config) -> None:
        """Configure the plugin after command line options are parsed."""
        print()
        self.config = config
        self.reporter = Reporter(self.config)

        try:
            check.use_log(self.reporter.log)
        finally:
            pass

        # Register markers if needed
        config.addinivalue_line(
            "markers", 
            "myplugin: mark test to be processed by myplugin"
        )
    
    @pytest.hookimpl
    def pytest_unconfigure(self, config: Config) -> None:
        """Clean up when pytest exits."""
        pass
    
    # ========== SESSION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        """Called after Session object has been created."""
        pass
    
    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        """Called after whole test run finished."""
        pass
        
    
    # ========== COLLECTION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_collection_modifyitems(self, config: Config, items: List[Item]) -> None:
        """
        Modify collected test items.
        This is one of the most commonly used hooks.
        """
        pass
    
    @pytest.hookimpl
    def pytest_generate_tests(self, metafunc) -> None:
        """
        Generate parametrized tests.
        Use this to dynamically create test parameters.
        """
        pass
    
    # ========== TEST EXECUTION HOOKS ==========

    @pytest.hookimpl(trylast=True)
    def pytest_runtest_protocol(self, item: Item, nextitem: Item):
        # -- Set verbosity back to the original value -------------------- #
        self.reporter.reporter_runtest_protocol()

    @pytest.hookimpl
    def pytest_runtest_setup(self, item: Item) -> None:
        """Called before each test setup."""
        self.reporter.reporter_runtest_setup()

    @pytest.hookimpl
    def pytest_runtest_call(self, item: Item) -> None:
        """Called before each test call."""
        self.reporter.reporter_runtest_call()

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item: Item, nextitem: Optional[Item]) -> None:
        """Called after each test teardown."""
        # -- TODO: This print should be set in the terminal reporter ------ #
        self.reporter.reporter_runtest_teardown()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item: Item, call: CallInfo):
        outcome = yield
        try:
            report: TestReport = outcome.get_result()

            # -- What this does: ------------------------------------------------ #
            # -- 1. Prevents 'Captured Log' To be printed when an error occurs -- #
            # -- ... 
            self.reporter.reporter_makereport(item, call, report)
        except: pass


    @pytest.hookimpl(trylast=True)
    def pytest_runtest_logreport(self, report: TestReport):
        self.reporter.reporter_runtest_logreport()

    # ========== REPORTING HOOKS ==========
    
    @pytest.hookimpl
    def pytest_report_header(self, config: Config, start_path: Path) -> Union[str, List[str]]:
        """Add information to the test report header."""
        pass
    
    @pytest.hookimpl
    def pytest_terminal_summary(self, terminalreporter, exitstatus: int, config: Config) -> None:
        """Add a section to the terminal summary reporting."""
        pass
    
    # ========== ERROR/WARNING HOOKS ==========
    
    @pytest.hookimpl
    def pytest_warning_recorded(self, warning_message: warnings.WarningMessage, when: str, nodeid: str, location: tuple) -> None:
        """Called when a warning is recorded."""
        pass
    
    @pytest.hookimpl
    def pytest_exception_interact(self, node, call: CallInfo, report: TestReport) -> None:
        """Called when an exception occurred and can be interacted with."""
        pass
    

# Plugin instance
_pytest_report_plugin = PytestReportPlugin()

def pytest_addoption(parser) -> None:
    """Add command-line options for the plugin."""
    group = parser.getgroup("pytest_report", "Pytest Report Options")

    group.addoption(
        "--report-tree",
        action="store",
        choices=["tree", "flat", "debug"],
        default='tree',
        help="It determines how the report file structure will be generated"
    )

    group.addoption(
        "--report-debug",
        action="store_true",
        default=False,
        help="Generate a report file structure easy for debuggig (overrides --report-tree to 'debug')"
    )

    group.addoption(
        "--show-capture-log",
        action="store_true",
        default=False,
        help="Shows the capture log when an 'error' is generated."
    )

    group.addoption(
        "--setup-level",
        action="store",
        choices=["debug", "info", "warning", "error", "critical"],
        default='warning',
        help="It determine the terminal log level at setup stage"
    )

    group.addoption(
        "--call-level",
        action="store",
        choices=["debug", "info", "warning", "error", "critical"],
        default='info',
        help="It determine the terminal log level at call stage"
    )

    group.addoption(
        "--procedure-report-html-template",
        action="store",
        default=None,
        help="Path to the Procedure HTML template"
    )


def pytest_configure(config):
    """Register the plugin instance."""
    if not hasattr(config, '_pytest_report_plugin'):
        config.pluginmanager.register(_pytest_report_plugin, "pytest-report")

def pytest_unconfigure(config):
    if config.pluginmanager.has_plugin("pytest_report"):
        config.pluginmanager.unregister(_pytest_report_plugin, "pytest_report")
