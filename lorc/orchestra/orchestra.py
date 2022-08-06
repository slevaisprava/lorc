import re
from re import Pattern

from lorc.orchestra import envelopes, templates

RE_COMMENTS: tuple[Pattern[str], ...] = (
    re.compile("(;.*)|(//.*)"),
    re.compile("/\\*.*\\*/", re.DOTALL)
)
RE_INSTRUMENTS: Pattern[str] = re.compile(
    "^(?P<izero>.*?)?^\\s*?instr\\s+(?P<inum>\\w+)(?P<ibody>.+?)^\\s*?endin", re.DOTALL + re.MULTILINE
)
RE_VOICES: Pattern[str] = re.compile(
    "^(?P<vzero>.*?)?^\\s*?(?P<vtype>[vme])(?P<vnum>\\d+):{(?P<vbody>.+?)}", re.DOTALL + re.MULTILINE
)
RE_INSTR_HAS_VOICE: Pattern[str] = re.compile("[vme]\\d+:{")
RE_K_VAR: Pattern[str] = re.compile("([^:_]\\bk[a-zA-Z0-9]*\\b)")
RE_KP_FIELD: Pattern[str] = re.compile("\\b(kp\\d+_v\\d+\\b)")
RE_VARIABLES_WITH_TILDA: Pattern[str] = re.compile("^\\s*?~.+?$", re.DOTALL + re.MULTILINE)
RE_TILDA_REPLACE: Pattern[str] = re.compile("~", re.DOTALL + re.MULTILINE)
RE_VARIABLES_WITHOUT_TILDA: Pattern[str] = re.compile("^\\s*?[^~]\\w.+?$", re.DOTALL + re.MULTILINE)


class Orchestra:
    @staticmethod
    def parse_instruments(src: str, orc_num: int):
        src = Orchestra.remove_comments(src)
        src, ftgens = Orchestra.parse_envs(src, str(orc_num))
        udo = Orchestra.parse_udo()
        orc: list[str, str] = [ftgens, udo]
        for instr in RE_INSTRUMENTS.finditer(src):
            ibody = instr.group("ibody")
            orc.append(instr.group("izero") or "\n")
            orc.append("instr\t" + instr.group("inum"))

            if not RE_INSTR_HAS_VOICE.search(ibody):
                orc.append(ibody)
                orc.append("endin\n")
                continue

            for voice in RE_VOICES.finditer(ibody):
                orc.append(voice.group("vzero") or "")
                code = parse_vars(
                    voice.group("vbody"),
                    voice.group("vnum"),
                    voice.group("vtype")
                )
                orc.append(code)
            orc.append("endin\n")
        return orc

    @staticmethod
    def remove_comments(src: str) -> str:
        for i in RE_COMMENTS:
            src = i.sub("", src)
        return src

    @staticmethod
    def parse_envs(src: str, orc_num: str) -> tuple[str, str]:
        env_obj = envelopes.ParseEnvelope(src, orc_num)
        src = env_obj.src
        return src, env_obj.ftgens

    @staticmethod
    def parse_udo():
        return "\n;Empty UDO\n"


def parse_vars(voice: str, voice_num: str, voice_type: str) -> str:
    code: str = RE_K_VAR.sub(f"\\t\\g<1>_v{voice_num}", voice)
    pfields = list(sorted(set(RE_KP_FIELD.findall(code))))
    if len(pfields) < 3:
        return ""
    tilda: str = "\n".join(RE_VARIABLES_WITH_TILDA.findall(code))
    tilda: str = RE_TILDA_REPLACE.sub("\\t", tilda)
    no_tilda: str = "\n".join(RE_VARIABLES_WITHOUT_TILDA.findall(code))
    template: str = getattr(templates, voice_type)
    code: str = template.format(
        voice_num,
        no_tilda,
        tilda,
        pfields[0],
        ", ".join(pfields[2:])
    )
    return code
