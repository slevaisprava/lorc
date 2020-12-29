import re
import hashlib

import numpy as np

from lorc.gens import my_module
from lorc import lru_files

TAB_DIR = 'envs'


class ParseEnvelope:
    lst = '(\\[.*?\\]\\s*(?:\\*\\s*\\d+)?)'
    re_table_data = re.compile(
        f'([+~]*?)\\s*{lst}\\s*,\\s*{lst}\\s*,\\s*{lst}'
    )
    re_white_space = re.compile('\\s+')

    cache = lru_files.LRUFiles(TAB_DIR)

    def __init__(self, src, orc_num):
        self.orc_num = orc_num
        self._src = src
        self.tab_num = 0

        self.table_records = dict()
        self._ftgens = []

    @property
    def ftgens(self):
        return '\n'.join(self._ftgens)

    @property
    def src(self):
        self._src = self.re_table_data.sub(self._replace_func, self._src)
        return self._src

    def _replace_func(self, obj: re.Match):
        self.tab_num += 1
        env_data = [self.re_white_space.sub('', s) for s in obj.groups()]
        env_name = f'gi_env_{self.orc_num}_{self.tab_num}'

        self._make_table_records(env_name, env_data)
        self._calc_env()

        return env_name

    def _make_table_records(self, env_name, env_data):
        hash_dig = self._hex_dig(env_data)
        env_data.append(env_name)

        if hash_dig in self.table_records:
            existing_name = self.table_records[hash_dig][4]
            self._ftgens.append(env_name + ' = ' + existing_name)
        else:
            self.table_records[hash_dig] = env_data
            ftgen23 = 'ftgen 0, 0, 0, -23'
            self._ftgens.append(
                f'{env_name} {ftgen23}, "{self.cache.path}/{hash_dig}"'
            )

    @staticmethod
    def _hex_dig(env_data):
        hash_object = hashlib.sha1(str(env_data).encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig[:20]

    def _calc_env(self):
        for key in self.table_records:
            if self.cache.in_cache(key):
                continue
            env_arg = [eval(val) for val in self.table_records[key][1:4]]
            env_arg[0] = np.array(env_arg[0], dtype=np.float)
            env_arg[1] = np.array(env_arg[1], dtype=np.int32)
            env_arg[2] = np.array(env_arg[2], dtype=np.float)

            if '+' in self.table_records[key][0]:
                env_arg.append(1)
            else:
                env_arg.append(0)
            if '~' in self.table_records[key][0]:
                res = my_module.cycle_env(*env_arg)
            else:
                res = my_module.env(*env_arg)

            self._write_result(res, key)

    def _write_result(self, res, key):
        np.savetxt(f'{self.cache.path}/{key}', res, fmt='%g')
        self.cache.put(key)


if __name__ == "__main__":
    SRC = '''
        table([123,23], [11,17], [5], 12, 78)
        table(+~[123,23], [11,17], [-5], 12, 78)
        table(~+[123,23], [11,17], [-5], 12, 78)
        table(~[123,23], [11,17], [-5], 12, 78)
    '''
    t = ParseEnvelope(SRC, 1)
    _ = t.src
