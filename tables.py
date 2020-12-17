import re
import hashlib


class ParseTables:
    lst = '(\\[.*?\\]\\s*(?:\\*\\s*\\d*)?)'
    re_table_data = re.compile(f'([+~]*?)\\s*{lst}\\s*,\\s*{lst}\\s*,\\s*{lst}')
    re_white_space = re.compile('\\s+')

    ftgen23 = '{} ftgen 0, 0, 0, -23, {}'

    def __init__(self, src, orc_num):
        self.orc_num = orc_num
        self.src = src
        self.tab_def = None
        self.tab_name = None
        self.tab_num = 0

        self.table_records = dict()
        self.ftgens = []

    def replace_table_definitions(self):
        self.src = self.re_table_data.sub(self._table_proc, self.src)
        return self.src, '\n'.join(self.ftgens)

    def _table_proc(self, obj: re.Match):
        self.tab_num += 1
        self.tab_def = [self.re_white_space.sub('', s) for s in obj.groups()]
        self.tab_name = f'gi_tab_{self.orc_num}_{self.tab_num}'
        self._make_table_record()
        return self.tab_name

    def _make_table_record(self):
        hash_dig = self._make_hash_dig()
        self.tab_def.append(self.tab_name)
        if hash_dig in self.table_records:
            existing_name = self.table_records[hash_dig][4]
            self.ftgens.append(self.tab_name + ' = ' + existing_name)
        else:
            self.table_records[hash_dig] = self.tab_def
            self.ftgens.append(self.ftgen23.format(self.tab_name, hash_dig))

    def _make_hash_dig(self):
        hash_object = hashlib.sha1(str(self.tab_def).encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig[:20]


class MakeTables:
    def __init__(self, data):
        pass


if __name__ == "__main__":
    SRC = '''
        table([123,23], [11,17], [5], 12, 78)
        table([123,23], [11, 16], [5], 12, 78)
        table(~+[123,23], [ 11 ,16], [ 5 ], 12, 78)
        table([123,23], [ 11 ,16], [ 5 ], 12, 78)
    '''
    t = ParseTables(SRC, 1)
    s, f = t.replace_table_definitions()
    print(t.table_records)
    print(s, f)
