import importlib
import gc

from lorc_csp.gens import my_module
from lorc_csp.vim import startup
from lorc_csp import lru_files
from lorc_csp import envelopes
from lorc_csp import templates
from lorc_csp import orchestra

def reload_modules():
    importlib.reload(startup)
    importlib.reload(my_module)
    importlib.reload(templates)
    importlib.reload(lru_files)
    importlib.reload(envelopes)
    importlib.reload(orchestra)
    gc.collect()
