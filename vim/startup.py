import importlib
import gc
import os

import vim

from lorc.gens import my_module
from lorc.vim import startup
from lorc import lru_files
from lorc import envelopes
from lorc import templates
from lorc import orchestra


def reload_modules():
    importlib.reload(startup)
    importlib.reload(my_module)
    importlib.reload(templates)
    importlib.reload(lru_files)
    importlib.reload(envelopes)
    importlib.reload(orchestra)
    gc.collect()
    print('Done')

def pr(txt):
    vim.command('call Term_Start()')
