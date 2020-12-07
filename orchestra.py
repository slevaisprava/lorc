import re
import time

import templates


class Orchestra:

    re_comments = (
        re.compile('(;.*)|(//.*)'),
        re.compile('/\\*.*\\*/', re.DOTALL)
    )
    re_instrs = re.compile(
        '^(?P<izero>.*?)?^\\s*?instr\\s+(?P<inum>\\w+)(?P<ibody>.+?)^\\s*?endin',
        re.DOTALL + re.MULTILINE
    )
    re_voices = re.compile(
        '^(?P<vzero>.*?)?^\\s*?(?P<vtype>[vme])(?P<vnum>\\d+):{(?P<vbody>.+?)}',
        re.DOTALL + re.MULTILINE
    )
    re_is_event_instr = re.compile('[vme]\\d+:{')
    re_tilda_search = re.compile('^\\s*?~.+?$', re.DOTALL + re.MULTILINE)
    re_tilda_replace = re.compile('~', re.DOTALL + re.MULTILINE)
    re_no_tilda = re.compile('^\\s*?[^~]\\w.+?$', re.DOTALL + re.MULTILINE)
    re_kvar = re.compile('([^:_]\\bk[a-zA-Z0-9]*\\b)')
    re_kp_field = re.compile('\\b(kp\\d+_v\\d+\\b)')

    def __init__(self, src):
        st1 = time.time()
        self._src = self._remove_comments(src)
        self._orchestra = self._split()
        st2 = time.time()
        self._time = st2 - st1

    @property
    def time(self):
        return self._time

    @property
    def orchestra(self):
        return self._orchestra

    def _remove_comments(self, src):
        for i in self.re_comments:
            src = i.sub('', src)
        return src

    def _split(self):
        orc = list()
        for instr in self.re_instrs.finditer(self._src):
            ibody = instr.group('ibody')
            orc.append(instr.group('izero') or '\n')  # tabs
            orc.append('instr\t' + instr.group('inum'))

            # Normal instruments
            if not self.re_is_event_instr.search(ibody):
                orc.append(ibody)
                orc.append('endin\n')
                continue

            for voice in self.re_voices.finditer(ibody):
                orc.append(voice.group('vzero') or '')
                code = self._change_kvars(
                    voice.group('vbody'),
                    voice.group('vnum'),
                    voice.group('vtype')
                )
                orc.append(code)
            orc.append('endin\n')
        return orc

    def _change_kvars(self, voice, vnum, vtype):
        code = self.re_kvar.sub(f'\\t\\g<1>_v{vnum}', voice)
        pfields = list(sorted(set(self.re_kp_field.findall(code))))

        if len(pfields) < 3:
            return ''

        tilda = '\n'.join(self.re_tilda_search.findall(code))
        tilda = self.re_tilda_replace.sub('\\t', tilda)
        no_tilda = '\n'.join(self.re_no_tilda.findall(code))
        template = getattr(templates, vtype)
        code = template.format(
            vnum,
            no_tilda,
            tilda,
            pfields[0],
            ', '.join(pfields[2:])
        )
        return code


if __name__ == "__main__":
    with open('sample.csp', 'r') as f:
        source = f.read()
    orch = Orchestra(source)
    with open('sample.orc', 'w') as f:
        f.writelines(orch.orchestra)
