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


path = os.path.realpath(__file__)
path = os.path.dirname(path)
vim_conf_file = os.path.join(path, 'startup.vim')

with open(vim_conf_file, 'r') as f:
    vim_script = f.read()
    vim.command(vim_script)


def pr():
    src = '\n'.join(vim.current.buffer[:])
    orch = orchestra.Orchestra(src, 1)
    with open('/dev/shm/sample.orc', 'w') as f:
        f.writelines(orch.orchestra)
    vim.command('call Term_Start()')

def pr1():
    envelopes.ParseEnvelope.cache._clear_cache()
