

from pytest_meta import meta
import os

from datetime import date, datetime

def get_hierarchy() -> list[str]:
    return meta.current_test.hierarchy

def get_test_index() -> str:
    return str(meta.current_test.test_index)

def get_testcase() -> str:
    return meta.current_test.testcase

class ReportPaths:
    MODE_TREE = 'tree'
    MODE_FLAT = 'flat'
    MODE_DEBUG = 'debug'

    def __init__(self, *args, **kwargs):
        self.root       = kwargs.get('root', './reports')
        self.tree_mode  = kwargs.get('tree_mode', 'tree')

    @property
    def now(self) -> str:
        return datetime.now().strftime("%H_%M_%S")

    @property
    def today(self) -> str:
        return date.today().strftime("%Y_%m_%d")

    @property
    def current_test_root_report_path(self) -> str:
        if self.tree_mode == self.MODE_TREE:
            return self.shape_path(*get_hierarchy())
        elif self.tree_mode == self.MODE_FLAT:
            return self.shape_path(self.get_flat_test_path())
        elif self.tree_mode == self.MODE_DEBUG:
            return self.shape_path('DEBUG', add_time=False)

        else:
            pass

    @property
    def logsetup_fname(self) -> str:
        if self.tree_mode == self.MODE_TREE:
            return self.shape_path(*get_hierarchy(), get_test_index(), 'setup', f'{get_testcase()}.log')
        elif self.tree_mode == self.MODE_FLAT:
            return self.shape_path(self.get_flat_test_path(), 'setup', f'{get_testcase()}.log')
        elif self.tree_mode == self.MODE_DEBUG:
            return self.shape_path('DEBUG', get_test_index(), 'setup', f'{get_testcase()}.log', add_time=False)
        else:
            pass

    @property
    def logcall_fname(self) -> str:
        if self.tree_mode == self.MODE_TREE:
            return self.shape_path(*get_hierarchy(), get_test_index(), f'{get_testcase()}.log')
        elif self.tree_mode == self.MODE_FLAT:
            return self.shape_path(self.get_flat_test_path(), f'{get_testcase()}.log')
        elif self.tree_mode == self.MODE_DEBUG:
            return self.shape_path('DEBUG', get_test_index(), f'{get_testcase()}.log', add_time=False)

        else:
            pass
    

    def get_flat_test_path(str) -> str:
        return '_'.join(get_hierarchy()) + f"::{get_testcase()}"

    def shape_path(self, *args, **kwargs) -> str:
        add_date: bool = kwargs.get('add_date', True)
        add_time: bool = kwargs.get('add_time', True)

        if add_date and add_time:
            return os.path.join(self.root, self.today, self.now, *args)
    
        if add_date and not add_time:
            return os.path.join(self.root, self.today, *args)

        if not add_date and add_time:
            return os.path.join(self.root, self.now, *args)
        
        return os.path.join(self.root, *args)