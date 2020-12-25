import re
import hashlib

import numpy as np

import my_module
import lru_files

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
        self.src = src
        self.env_def = None
        self.env_name = None
        self.tab_num = 0

        self.table_records = dict()
        self.ftgens = []

    def replace_env_readers(self):
        self.src = self.re_table_data.sub(self._env_proc, self.src)
        self.ftgens = '\n'.join(self.ftgens)

    def _env_proc(self, obj: re.Match):
        self.tab_num += 1
        self.env_def = [self.re_white_space.sub('', s) for s in obj.groups()]
        self.env_def[0] = ''.join(sorted(self.env_def[0]))

        self.env_name = f'gi_env_{self.orc_num}_{self.tab_num}'
        self._make_table_record()
        return self.env_name

    def _make_table_record(self):
        hash_dig = self._make_hash_dig()
        self.env_def.append(self.env_name)
        if hash_dig in self.table_records:
            existing_name = self.table_records[hash_dig][4]
            self.ftgens.append(self.env_name + ' = ' + existing_name)
        else:
            self.table_records[hash_dig] = self.env_def
            ftgen = 'ftgen 0, 0, 0, -23'
            self.ftgens.append(
                f'{self.env_name} {ftgen}, "{self.cache.path}/{hash_dig}"'
            )

    def _make_hash_dig(self):
        hash_object = hashlib.sha1(str(self.env_def).encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig[:20]


class MakeEnvelopes:
    def __init__(self, table_records, cache):
        self.cache = cache
        self.table_records = table_records
        self.make_env_functions_args()

    def make_env_functions_args(self):
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

            self.write_result(res, key)

    def write_result(self, res, key):
        np.savetxt(f'{self.cache.path}/{key}', res, fmt='%g')
        self.cache.put(key)


if __name__ == "__main__":
    SRC = '''
        table([123,23], [11,17], [5], 12, 78)
        table(~[123,23], [11,17], [-5], 12, 78)
        table(~+[123,23], [11,17], [-5], 12, 78)
        table(~[123,23], [11,17], [-5], 12, 78)
    '''
    t = ParseEnvelope(SRC, 1)
    t.replace_env_readers()
    m = MakeEnvelopes(t.table_records, t.cache)
