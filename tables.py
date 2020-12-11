import re
import hashlib

class ParseTables:
    lst = '(\\[.*?\\]\\s*(?:\\*\\s*\\d*)?)'
    re_table_data = re.compile(f'([~]?)\\s*{lst}\\s*,\\s*{lst}\\s*,\\s*{lst}')

    def __init__(self, src, orc_num):
        self.orc_num = orc_num
        self.src = src

        self.tab_num = 0
        self.tab_name = ''
        self.table_records = []

        self._parse_table_data()
        MakeTables(self.table_records)

    def _parse_table_data(self):
        self.src = self.re_table_data.sub(self._replace_table_data, self.src)

    def _replace_table_data(self, obj: re.Match):
        self.tab_num += 1
        data = obj.groups()
        self._make_table_record(data)
        self.tab_name = f'gi_tab_{self.orc_num}_{self.tab_num}'
        return self.tab_name

    def _make_table_record(self, data):
        hash_sum = self._make_hash_sum(str(data))
        data = list(data)
        data.append(hash_sum)
        data.append(self.tab_name)
        self.table_records.append(data)

    @staticmethod
    def _make_hash_sum(data):
        hash_object = hashlib.sha1(data.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig[:20]

class MakeTables:
    def __init__(self, data):
        pass


if __name__ == "__main__":
    SRC = '''
        table(~[123,23], [11,17], [5], 12, 78)
        table([123,23], [11,16], [5], 12, 78)
        table([123,23], [11,16], [5], 12, 78)
    '''
    t = ParseTables(SRC, 1)
    print(t.table_records)
    print(t.src)
