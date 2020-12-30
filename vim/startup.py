import importlib
import gc
import os

import vim

from lorc import lru_files, envelopes, templates, orchestra
from lorc.gens import my_module


BASE_DIR = '/dev/shm/csound'


def make_path(path):
    path = os.path.join(BASE_DIR, path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def load_vim_scripts():
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    vim_conf_file = os.path.join(path, 'startup.vim')

    with open(vim_conf_file, 'r') as f:
        vim_script = f.read()
        vim.command(vim_script)


def reload_modules():
    from lorc.vim  import startup
    importlib.reload(startup)
    importlib.reload(my_module)
    importlib.reload(templates)
    importlib.reload(lru_files)
    importlib.reload(envelopes)
    importlib.reload(orchestra)
    gc.collect()
    print('Done')


def start_single_orc():
    src = '\n'.join(vim.current.buffer[:])
    orc = orchestra.Orchestra(src, 1)
    tmp_name = os.path.join(
        ORC_TMP_DIR, 
        os.path.basename(vim.current.buffer.name) + '.orc'
    )
    with open(tmp_name, 'w') as f:
        f.writelines(orc.orchestra)
    cmd = vim.current.buffer[0].lstrip(';').split()
    cmd.append(tmp_name)
    vim.command(f'call Term_Start({cmd})')

def on_csound_close():
    envelopes.ParseEnvelope.cache._clear_cache()


load_vim_scripts()
ORC_TMP_DIR = make_path('')
ORC_TMP_DIR = make_path('orcs')
