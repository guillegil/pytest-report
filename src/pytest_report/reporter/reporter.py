
import os
from pytest import Item, Config, Session, TestReport, CallInfo
from _pytest.runner import TestReport

from jinja2 import Environment, FileSystemLoader, ModuleLoader
import importlib.resources

from pathlib import Path

from .paths import ReportPaths
from .terminal_reporter import TerminalReporter
from pytest_meta import meta

from advanced_logger import AdvancedLogger

class Reporter:
    def __init__(self, config: Config, *args, **kwargs):
        self.__config  = config
        self.__options = self.__config.option

        self.__report_path: str = config.getoption('--report-path', './reports')
        self.__report_tree: str = config.getoption('--report-tree', 'tree')

        self.__terminal_reporter = TerminalReporter(self.__config, *args, **kwargs)

        self.__log = AdvancedLogger('pytest_report')

        self.paths = ReportPaths(root=self.__report_path, tree_mode=self.__report_tree)

        # -- Set default options ---------------------------------- #
        self.__options.verbose = -1
        self.__options.quiet = 2
        self.__options.tbstyle = 'short'

    @property
    def report_path(self) -> str:
        return self.__report_path

    @property
    def report_tree(self) -> str:
        return self.__report_tree

    @property
    def terminal_reporter(self) ->TerminalReporter:
        return self.__terminal_reporter

    @property
    def log(self) -> AdvancedLogger:
        return self.__log


    def reporter_runtest_protocol(self) -> None:
        self.terminal_reporter.configure_report_protocol()

    def reporter_runtest_setup(self) -> None:
        # -- Configure terminal reporter on setup stage ----------------- #
        self.terminal_reporter.configure_report_setup()

        # -- Create a log file for for the setup ------------------------ #
        self.log.init_file_handler('stage_file_handler', self.paths.logsetup_fname, level='info')

    def reporter_runtest_call(self) -> None:
        # -- Configure terminal reporter on call stage ------------------ #
        self.terminal_reporter.configure_report_call()

        # -- Create a log file for for the call ------------------------- #
        self.log.init_file_handler('stage_file_handler', self.paths.logcall_fname, level='info')

    def reporter_makereport(
        self, 
        item    : Item,
        call    : CallInfo, 
        report  : TestReport
    ) -> None:
        self.terminal_reporter.manage_captured_log(report)

    def reporter_runtest_logreport(self) -> None:
        self.generate_test_procedure_html()

    def generate_test_report_html(self) -> None:
        pass

    def generate_test_procedure_html(self) -> None:
        # Load template from the current folder
        with importlib.resources.path("pytest_report.jinja", "procedure_template.html.jinja") as template_path:
            env = Environment(loader=FileSystemLoader(template_path.parent))
            template = env.get_template("procedure_template.html.jinja")

        # Render with the dictionary
        output = template.render(test_procedure=self.log.test_procedure)

        # Save the output HTML
        with open(f"{self.paths.current_test_root_report_path}/test_procedure.html", "w", encoding="utf-8") as f:
            f.write(output)