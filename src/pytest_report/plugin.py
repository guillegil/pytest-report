"""
Modern pytest plugin template with clean hook implementations.
"""
import pytest
from pytest import Item, Config, Session, TestReport, CallInfo
from pathlib import Path
from typing import Optional, List, Union, Any
import warnings

from .reporter.reporter import Reporter

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
        self.config: Optional[Config] = None
        self.verbose: bool = False
    
        self.reporter = None
    
    # ========== CONFIGURATION HOOKS ==========
    @pytest.hookimpl
    def pytest_configure(self, config: Config) -> None:
        """Configure the plugin after command line options are parsed."""
        print()
        
        options: dict = config.option

        options.verbose = -2
        options.quiet = 2

        options.tbstyle='short'

        self.config = config
        self.verbose = config.getoption("--reportplug-verbose")

        if self.verbose:
            print("🔧 MyPlugin configured")
        
        self.reporter = Reporter(config)

        # Register markers if needed
        config.addinivalue_line(
            "markers", 
            "myplugin: mark test to be processed by myplugin"
        )
    
    @pytest.hookimpl
    def pytest_unconfigure(self, config: Config) -> None:
        """Clean up when pytest exits."""
        if self.verbose:
            print("🔧 MyPlugin unconfigured")
    
    
    # ========== SESSION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_sessionstart(self, session: Session) -> None:
        """Called after Session object has been created."""
        if self.verbose:
            print(f"🚀 Test session started")
        
        
        # Initialize session-level resources
        # Example: self.mytool.setup_session()
    
    @pytest.hookimpl
    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        """Called after whole test run finished."""
        if self.verbose:
            print(f"🏁 Test session finished with exit status: {exitstatus}")
        
        # Clean up session-level resources
        # Example: self.mytool.cleanup_session()
    
    # ========== COLLECTION HOOKS ==========
    
    @pytest.hookimpl
    def pytest_collection_modifyitems(self, config: Config, items: List[Item]) -> None:
        """
        Modify collected test items.
        This is one of the most commonly used hooks.
        """
        if self.verbose:
            print(f"📝 Processing {len(items)} collected test items")
        
        # Example: Add markers, skip tests, reorder items, etc.
        for item in items:
            # Example: Add marker to all tests in certain directories
            if "integration" in str(item.fspath):
                item.add_marker(pytest.mark.integration)
            
            # Example: Skip tests based on custom logic
            if hasattr(item, "function") and hasattr(item.function, "__name__"):
                if item.function.__name__.startswith("skip_"):
                    item.add_marker(pytest.mark.skip(reason="Marked for skipping"))
    
    @pytest.hookimpl
    def pytest_generate_tests(self, metafunc) -> None:
        """
        Generate parametrized tests.
        Use this to dynamically create test parameters.
        """
        if self.verbose:
            print(f"⚙️ Generating tests for: {metafunc.function.__name__}")
        
        # Example: Parametrize tests based on custom logic
        if "sample_data" in metafunc.fixturenames:
            # Generate test data dynamically
            test_data = ["data1", "data2", "data3"]
            metafunc.parametrize("sample_data", test_data)
    
    # ========== TEST EXECUTION HOOKS ==========

    @pytest.hookimpl
    def pytest_runtest_protocol(self, item: Item, nextitem: Item):
        # -- Set verbosity back to the original value -------------------- #
        self.config.option.verbose = 1

    @pytest.hookimpl
    def pytest_runtest_setup(self, item: Item) -> None:
        """Called before each test setup."""
        if self.verbose:
            print(f"🔧 Setting up test: {item.nodeid}")
        
        # Example: Custom setup logic
        # self.mytool.setup_test(item)

    @pytest.hookimpl
    def pytest_runtest_call(self, item: Item) -> None:
        """Called before each test call."""
        print()
        if self.verbose:
            print(f"🔧 Setting up test: {item.nodeid}")
        
        # Example: Custom setup logic
        # self.mytool.setup_test(item)

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item: Item, nextitem: Optional[Item]) -> None:
        """Called after each test teardown."""
        print('\n')
        if self.verbose:
            print(f"🧹 Tearing down test: {item.nodeid}")
        
        # Example: Custom teardown logic
        # self.mytool.teardown_test(item)


    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item: Item, call: CallInfo):
        outcome = yield
        report: TestReport = outcome.get_result()

        self.reporter.report_makereport(item, call, report)


    # ========== REPORTING HOOKS ==========
    
    @pytest.hookimpl
    def pytest_report_header(self, config: Config, start_path: Path) -> Union[str, List[str]]:
        """Add information to the test report header."""
        if self.verbose:
            return [
                f"MyPlugin: Enabled with verbose output",
                f"MyOption: {config.getoption('--myoption')}"
            ]
        return []
    
    @pytest.hookimpl
    def pytest_terminal_summary(self, terminalreporter, exitstatus: int, config: Config) -> None:
        """Add a section to the terminal summary reporting."""
        if self.verbose:
            terminalreporter.write_sep("=", "MyPlugin Summary")
            terminalreporter.write_line("MyPlugin executed successfully")
            
            # Example: Add custom statistics
            # passed = len([r for r in terminalreporter.stats.get('passed', [])])
            # terminalreporter.write_line(f"MyPlugin processed {passed} passed tests")
    
    # ========== ERROR/WARNING HOOKS ==========
    
    @pytest.hookimpl
    def pytest_warning_recorded(self, warning_message: warnings.WarningMessage, when: str, nodeid: str, location: tuple) -> None:
        """Called when a warning is recorded."""
        if self.verbose:
            print(f"⚠️ Warning in {nodeid}: {warning_message.message}")
    
    @pytest.hookimpl
    def pytest_exception_interact(self, node, call: CallInfo, report: TestReport) -> None:
        """Called when an exception occurred and can be interacted with."""
        if self.verbose:
            print(f"💥 Exception in {node.nodeid}: {call.excinfo}")
    
    # ========== FIXTURES ==========
    
    @pytest.fixture
    def myplugin_tool(self):
        """Provide access to MyTool as a fixture."""
        return self.mytool
    
    @pytest.fixture
    def sample_data(self):
        """Sample fixture that can be used in tests."""
        return {"key": "value", "number": 42}




# Plugin instance
_pytest_report_plugin = PytestReportPlugin()

def pytest_addoption(parser) -> None:
    """Add command-line options for the plugin."""
    group = parser.getgroup("pytest_report", "Pytest Report Options")

    parser.addoption(
        "--show-capture-log",
        action="store_true",
        default=False,
        help="Shows the capture log when an 'error' is generated."
    )

    parser.addoption(
        "--reportplug-verbose",
        action="store_true",
        default=False,
        help="Enable verbose output for myplugin"
    )
    parser.addoption(
        "--remove-extra-return-before-call",
        action="store_false",
        default=False,
        help="Custom option for the plugin"
    )


def pytest_configure(config):
    """Register the plugin instance."""
    if not hasattr(config, '_pytest_report_plugin'):
        config.pluginmanager.register(_pytest_report_plugin, "pytest-report")

# def pytest_unconfigure(config):
#     if config.pluginmanager.has_plugin("pytest_report"):
#         config.pluginmanager.unregister(_pytest_report_plugin, "pytest_report")





# # Export fixtures
# report_tool = _pytest_report_plugin.myplugin_tool
# sample_data = _pytest_report_plugin.sample_data
