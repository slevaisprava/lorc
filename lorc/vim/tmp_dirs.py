import os

BASE_DIR = '/Users/es/ttmp'

def make_path(path):
    path = os.path.join(BASE_DIR, path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


BASE_PATH = make_path('')
ORC_TMP_PATH = make_path('orcs')
LRU_TMP_PATH = make_path('envs')
