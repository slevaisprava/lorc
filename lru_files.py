import os
from collections import OrderedDict

BASE_CACHE_DIR = '/dev/shm/csound'
CAPACITY = 20


class LRUFiles:
    def __init__(self, path):
        self._path = self.__class__.make_path(path)
        self._cache = self._make_cache()

    @property
    def path(self):
        return self._path

    @staticmethod
    def make_path(path):
        path = os.path.join(BASE_CACHE_DIR, path)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _make_cache(self):
        files = os.listdir(self._path)
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


if __name__ == "__main__":
    lru1 = LRUFiles('envs')
    print(lru1._cache)
