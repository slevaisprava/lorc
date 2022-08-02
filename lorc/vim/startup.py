import importlib
import gc
import os

from lorc.vim import tmp_dirs
from lorc import lru_files, envelopes, templates, orchestra, vim
from lorc.gens import my_module


def load_vim_scripts():
    path = os.path.realpath(__file__)
    path = os.path.dirname(path)
    vim_conf_file = os.path.join(path, 'startup.vim')

    with open(vim_conf_file, 'r') as f:
        vim_script = f.read()
        vim.command(vim_script)


def reload_modules():
    importlib.reload(tmp_dirs)
    importlib.reload(startup)
    importlib.reload(my_module)
    importlib.reload(templates)
    importlib.reload(lru_files)
    importlib.reload(envelopes)
    importlib.reload(orchestra)
    gc.collect()
    print('Done')


def start_single_orc():
    buf = vim.current.buffer

    orc = make_orc(buf)
    orc_name = save_orc(buf, orc)
    cmd = make_cmd(buf, orc_name)

    vim.command(f'call Term_Start({cmd})')


def make_orc(buf):
    src = '\n'.join(buf[:])
    orc = orchestra.Orchestra(src, 1)
    return orc


def save_orc(buf, orc):
    orc_name = os.path.join(
        tmp_dirs.ORC_TMP_PATH, 
        os.path.basename(buf.name) + '.orc'
    )
    with open(orc_name, 'w') as f:
        f.writelines(orc.orchestra)
    return orc_name


def make_cmd(buf, orc_name):
    cmd = buf[0].lstrip(';').split()
    cmd.append(orc_name)
    return cmd


def on_csound_close():
    envelopes.ParseEnvelope.cache._clear_cache()


load_vim_scripts()
