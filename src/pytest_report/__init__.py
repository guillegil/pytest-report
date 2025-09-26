# src/pytest_report/__init__.py
from advanced_logger import AdvancedLogger
from .reporter.reporter import reporter

log: AdvancedLogger = AdvancedLogger('pytest_report_logger_instance')

__all__ = ['log', 'reporter']
__version__ = '0.1.0'