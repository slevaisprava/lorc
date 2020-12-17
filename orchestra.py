import re

import templates
import envelopes


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

    def __init__(self, src, orc_num):
        self.src = src
        self.orc_num = orc_num

        self._parse_comments()

        env_obj = envelopes.ParseEnvelope(self.src, self.orc_num)
        env_obj.replace_env_readers()
        envelopes.MakeEnvelopes(env_obj.table_records)

        self._orchestra = self._split_instrs(env_obj.ftgens, ';udo')

    @property
    def orchestra(self):
        return self._orchestra

    def _parse_comments(self):
        for i in self.re_comments:
            self.src = i.sub('', self.src)

    def _split_instrs(self, envs, udo):
        orc = [envs, udo]
        for instr in self.re_instrs.finditer(self.src):
            ibody = instr.group('ibody')
            orc.append(instr.group('izero') or '\n')
            orc.append('instr\t' + instr.group('inum'))

            # Normal instruments
            if not self.re_is_event_instr.search(ibody):
                orc.append(ibody)
                orc.append('endin\n')
                continue

            # Event instruments
            for voice in self.re_voices.finditer(ibody):
                orc.append(voice.group('vzero') or '')
                code = self._parse_vars(
                    voice.group('vbody'),
                    voice.group('vnum'),
                    voice.group('vtype')
                )
                orc.append(code)
            orc.append('endin\n')
        return orc

    def _parse_vars(self, voice, vnum, vtype):
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
    with open('csound/sample.csp', 'r') as f:
        source = f.read()
    orch = Orchestra(source, 1)
    with open('csound/sample.orc', 'w') as f:
        f.writelines(orch.orchestra)
