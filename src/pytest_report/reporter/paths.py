

from pytest_meta import meta
import os

class ReportPaths:
    MODE_TREE = 'tree'
    MODE_FLAT = 'flat'
    MODE_DEBUG = 'debug'

    def __init__(self, *args, **kwargs):
        self.root       = kwargs.get('root', './reports')
        self.tree_mode  = kwargs.get('tree_mode', 'tree')

    @property
    def now(self) -> str:
        pass

    @property
    def today(self) -> str:
        pass

    @property
    def logsetup_fname(self) -> str:
        if self.tree_mode == self.MODE_TREE:
            return self.shape_path(*meta.hierarchy, str(meta.testindex), 'setup', f'{meta.testcase}.log')
        elif self.tree_mode == self.MODE_FLAT:
            pass
        elif self.tree_mode == self.MODE_DEBUG:
            pass
        else:
            pass

    @property
    def logcall_fname(self) -> str:
        if self.tree_mode == self.MODE_TREE:
            return self.shape_path(*meta.hierarchy, str(meta.testindex), f'{meta.testcase}.log')
        elif self.tree_mode == self.MODE_FLAT:
            return self.shape_path('DEBUG', str(meta.testindex))
        elif self.tree_mode == self.MODE_DEBUG:
            pass
        else:
            pass
    
    def shape_path(self, *args) -> str:
        return os.path.join(self.root, *args)