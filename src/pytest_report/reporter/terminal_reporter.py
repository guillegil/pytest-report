
import pytest
from pytest import Item, Config, Session, TestReport, CallInfo
from _pytest.runner import TestReport

class TerminalReporter:
    def __init__(self, config: Config, *args, **kwargs):
        self.__config  : Config = config
        self.__options = self.__config.option
        
        self.__show_captured_log_on_error: bool = config.getoption('--show-capture-log', False)

    def set_verbosity(self, verbosity: int) -> None:
        self.__options.verbose = verbosity

    def configure_report_protocol(self) -> None:
        self.set_verbosity(1)

    def configure_report_setup(self) -> None:
        print()
    
    def configure_report_call(self) -> None:
        print()

    def configure_report_teardown(self) -> None:
        print()

    def __show_captured_log(self, section_header: str) -> bool:        
        if self.__show_captured_log_on_error:
            return True

        header_is_str: bool = isinstance(section_header, str)
        has_captured_log: bool = section_header.lower().startswith("captured log")

        return (not header_is_str and has_captured_log)

    def manage_captured_log(self, report: TestReport) -> None:
        # Newer pytest: captured sections live directly on the report
        if not report.failed:
            return

        # Newer pytest: captured sections live directly on the report
        if hasattr(report, "sections") and report.sections:
            report.sections = [
                (section_header, section_content)

                for (section_header, section_content) 
                    in report.sections if self.__show_captured_log(section_header)
            ]
