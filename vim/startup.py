import importlib
import gc
import os

import vim

from lorc import lru_files, envelopes, templates, orchestra
from lorc.gens import my_module
from lorc.vim  import startup


def load_vim_scripts():
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    vim_conf_file = os.path.join(path, 'startup.vim')

    with open(vim_conf_file, 'r') as f:
        vim_script = f.read()
        vim.command(vim_script)


def reload_modules():
    importlib.reload(startup)
    importlib.reload(my_module)
    importlib.reload(templates)
    importlib.reload(lru_files)
    importlib.reload(envelopes)
    importlib.reload(orchestra)
    gc.collect()
    print('Done')


def start_single_orc(b):
    src = '\n'.join(vim.current.buffer[:])
    orch = orchestra.Orchestra(src, 1)

    with open('/dev/shm/sample.orc', 'w') as f:
        f.writelines(orch.orchestra)

    cmd = vim.current.buffer[0].lstrip(';').split()
    vim.command(f'call Term_Start({cmd})')


def pr1():
    envelopes.ParseEnvelope.cache._clear_cache()


load_vim_scripts()
