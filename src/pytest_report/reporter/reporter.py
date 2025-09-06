
from pytest import Item, Config, Session, TestReport, CallInfo
from _pytest.runner import TestReport

from .terminal_reporter import TerminalReporter

class Reporter:
    def __init__(self, config: Config, *args, **kwargs):
        self.__terminal_reporter = TerminalReporter(config, *args, **kwargs)
    
    @property
    def terminal_reporter(self) ->TerminalReporter:
        return self.__terminal_reporter
    
    def report_makereport(
        self, 
        item    : Item,
        call    : CallInfo, 
        report  : TestReport
    ) -> None:
        self.terminal_reporter.manage_captured_log(report)