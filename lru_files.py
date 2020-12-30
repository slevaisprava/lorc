import os
from collections import OrderedDict

from lorc.vim import tmp_dirs

CAPACITY = 20


class LRUFiles:
    def __init__(self):
        self._path = tmp_dirs.LRU_TMP_PATH
        self._cache = self._make_cache()

    @property
    def path(self):
        return self._path

    def _make_cache(self):
        try:
            files = os.listdir(self._path)
        except FileNotFoundError:
            return OrderedDict()
        else:
            return OrderedDict.fromkeys(files)

    def in_cache(self, hex_dig):
        if hex_dig in self._cache:
            self._cache.move_to_end(hex_dig)
            return True
        return False

    def put(self, hex_dig):
        self._cache[hex_dig] = None
        self._cache.move_to_end(hex_dig)

    def _clear_cache(self):
        cache_len = len(self._cache)
        if cache_len > CAPACITY:
            for _ in range(cache_len-CAPACITY):
                file_name = self._cache.popitem(last=False)[0]
                os.remove(os.path.join(self._path, file_name))
