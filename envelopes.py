import re
import hashlib


class ParseEnvelope:
    lst = '(\\[.*?\\]\\s*(?:\\*\\s*\\d*)?)'
    re_table_data = re.compile(f'([+~]*?)\\s*{lst}\\s*,\\s*{lst}\\s*,\\s*{lst}')
    re_white_space = re.compile('\\s+')


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
            self.ftgens.append(f'{self.env_name} ftgen 0, 0, 0, -23, {hash_dig}')

    def _make_hash_dig(self):
        hash_object = hashlib.sha1(str(self.env_def).encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig[:20]


class MakeEnvelopes:
    def __init__(self, data):
        pass


if __name__ == "__main__":
    SRC = '''
        table([123,23], [11,17], [5], 12, 78)
        table([123,23], [11, 16], [5], 12, 78)
        table(~+[123,23], [ 11 ,16], [ 5 ], 12, 78)
        table([123,23], [ 11 ,16], [ 5 ], 12, 78)
    '''
    t = ParseEnvelope(SRC, 1)
    t.replace_env_readers()
    print(t.table_records)
    print(t.src)
    print(t.ftgens)
