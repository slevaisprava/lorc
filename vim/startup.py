import importlib
import gc
import os

import vim

from lorc import my_module
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


def pr(txt):
    print(txt, os.getcwd())
    vim.command('call Start_Csound_Term()')
