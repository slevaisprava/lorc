import os
from collections import OrderedDict

BASE_CACHE_DIR = '/dev/shm/csound'
CAPACITY = 20


class LRUFiles:
    def __init__(self, path):
        self.path = self.__class__.make_path(path)
        self.cache = self.__class__.make_cache(self.path)

    @staticmethod
    def make_path(path):
        path = os.path.join(BASE_CACHE_DIR, path)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def make_cache(path):
        files = os.listdir(path)
        return OrderedDict.fromkeys(files)

    def in_cache(self, hex_dig):
        if hex_dig in self.cache:
            self.cache.move_to_end(hex_dig)
            return True
        return False

    def put(self, hex_dig):
        self.cache[hex_dig] = None
        self.cache.move_to_end(hex_dig)
        self.clear_cache()

    def clear_cache(self):
        cache_len = len(self.cache)
        if cache_len > CAPACITY:
            for _ in range(cache_len-CAPACITY):
                file_name = self.cache.popitem(last=False)[0]
                os.remove(os.path.join(self.path, file_name))


LRUFiles.make_path(BASE_CACHE_DIR)


if __name__ == "__main__":
    lru1 = LRUFiles('envs')
    print(lru1.cache)
