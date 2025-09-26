
import os
from pytest import Item, Config, Session, TestReport, CallInfo
from _pytest.runner import TestReport

from jinja2 import Environment, FileSystemLoader, DictLoader, TemplateNotFound
import importlib.resources

from pathlib import Path

from .paths import ReportPaths
from .terminal_reporter import TerminalReporter
from pytest_meta import meta

from advanced_logger import AdvancedLogger

DEFAULT_TEMPLATE_NAME = "procedure_template.html.jinja"
DEFAULT_PACKAGE = "pytest_report.jinja"

class Reporter:
    def __init__(self, config: Config, *args, **kwargs):
        self.__config  = config
        self.__options = self.__config.option

        self.__report_path: str = config.getoption('--report-path', os.path.join('.', 'reports'))
        self.__report_tree: str = config.getoption('--report-tree', 'tree')

        self.__setup_level : int = config.getoption('--setup-level', 'warning')
        self.__call_level  : int = config.getoption('--call-level', 'info')

        self.__procedure_template_file: str = config.getoption('--procedure-report-html-template', None)

        self.__terminal_reporter = TerminalReporter(self.__config, *args, **kwargs)

        self.__log = AdvancedLogger('pytest_report_logger_instance')

        # -- TODO: This should be done by the terminal reporter --------------------- #
        self.__log.init_term_handler('pytest_report_term_handler', level='info')

        self.paths = ReportPaths(root=self.__report_path, tree_mode=self.__report_tree)

        # -- Set meta values for reporting ------------------------ #
        meta.root_report_path = self.paths.root

        # -- Set default options ---------------------------------- #
        self.__options.verbose = -1
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
        
        meta.current_test.report_path = self.paths.current_testcase
        meta.current_test.report_path = self.paths.current_testcase_run

    def reporter_runtest_setup(self) -> None:
        # -- Configure terminal reporter on setup stage ----------------- #
        self.terminal_reporter.configure_report_setup()
      
        # -- Set the term level for the setup --------------------------- #
        self.log.set_handler_level('pytest_report_term_handler', level=self.__setup_level)

        # -- Create a log file for for the setup ------------------------ #
        self.log.init_file_handler('stage_file_handler', self.paths.logsetup_fname, level='info')

    def reporter_runtest_call(self) -> None:  
        # -- Configure terminal reporter on call stage ------------------ #
        self.terminal_reporter.configure_report_call()

        # -- Set the term level for the call ---------------------------- #
        self.log.set_handler_level('pytest_report_term_handler', level=self.__call_level)

        # -- Create a log file for for the call ------------------------- #
        self.log.init_file_handler('stage_file_handler', self.paths.logcall_fname, level=self.__call_level)

        self.log.init_procedure_log_handler('procedure_file_handler', self.paths.logproc_fname)
        self.log.reset_steps()

    def reporter_runtest_teardown(self) -> None:
        self.terminal_reporter.configure_report_teardown()

    def reporter_makereport(
        self, 
        item    : Item,
        call    : CallInfo, 
        report  : TestReport
    ) -> None:
        self.terminal_reporter.manage_captured_log(report)

        if meta.current_stage == 'teardown':
            self.generate_test_procedure_html()
    


    def reporter_runtest_logreport(self) -> None:
      if meta.current_stage == 'call':
        try:
            if meta.current_test.current_run.call.failed:
                Path(self.paths.current_testcase_run).rename(f'{self.paths.current_testcase_run}_F')

            if meta.current_test.current_run.call.passed:
                Path(self.paths.current_testcase_run).rename(f'{self.paths.current_testcase_run}_P')
        except:
            pass 

    def generate_test_report_html(self) -> None:
        pass

    def _load_template(self):
        # Case 1: user provided a custom path
        if self.__procedure_template_file:
            path = os.fspath(self.__procedure_template_file)
            if os.path.isdir(path):
                # Treat as directory containing the default template name
                env = Environment(loader=FileSystemLoader(path))
                try:
                    return env.get_template(DEFAULT_TEMPLATE_NAME)
                except TemplateNotFound:
                    raise FileNotFoundError(
                        f"Template '{DEFAULT_TEMPLATE_NAME}' not found in directory: {path}"
                    )
            elif os.path.isfile(path):
                # Treat as a full file path
                env = Environment(loader=FileSystemLoader(os.path.dirname(path)))
                return env.get_template(os.path.basename(path))
            else:
                raise FileNotFoundError(f"Template path does not exist: {path}")

        # Case 2: load default template from package resources
        try:
            # Robust for zip/egg: read text and feed via DictLoader
            content = importlib.resources.files(DEFAULT_PACKAGE).joinpath(DEFAULT_TEMPLATE_NAME).read_text(encoding="utf-8")
            env = Environment(loader=DictLoader({DEFAULT_TEMPLATE_NAME: content}))
            return env.get_template(DEFAULT_TEMPLATE_NAME)
        except (FileNotFoundError, ModuleNotFoundError, UnicodeDecodeError) as e:
            # Fallback: try filesystem loader with a real path if available
            try:
                with importlib.resources.as_file(
                    importlib.resources.files(DEFAULT_PACKAGE).joinpath(DEFAULT_TEMPLATE_NAME)
                ) as template_path:
                    env = Environment(loader=FileSystemLoader(template_path.parent))
                    return env.get_template(template_path.name)
            except Exception:
                raise RuntimeError(
                    f"Could not load default template '{DEFAULT_TEMPLATE_NAME}' from '{DEFAULT_PACKAGE}': {e}"
                )

    def generate_test_procedure_html(self) -> None:
        # Load template from the current folder

        template = self._load_template()

        # Render with the dictionary
        output = template.render(test_procedure=self.log.test_procedure)

        # Save the output HTML
        procedure_path = os.path.join(self.paths.current_testcase, 'test_procedure.html')

        with open(procedure_path, "w", encoding="utf-8") as f:
            f.write(output)