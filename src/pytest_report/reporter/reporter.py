
from pytest import Item, Config, Session, TestReport, CallInfo
from _pytest.runner import TestReport

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

        self.__terminal_reporter = TerminalReporter(config, *args, **kwargs)

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

    def _report_setup(self) -> None:
        self.log.init_file_handler('stage_file_handler', self.paths.logsetup_fname, level='info')

    def _report_call(self) -> None:
        self.log.init_file_handler('stage_file_handler', self.paths.logcall_fname, level='info')

        self.log.info('This is a test')

    def report_stage(self) -> None:
        if meta.stage == 'setup':
            self._report_setup()
        
        if meta.stage == 'call':
            self._report_call()

    def report_makereport(
        self, 
        item    : Item,
        call    : CallInfo, 
        report  : TestReport
    ) -> None:
        self.terminal_reporter.manage_captured_log(report)
    

    def generate_test_report_html(self, path: str) -> None:
        pass

    def generate_test_procedure_html(self, path: str) -> None:
        pass