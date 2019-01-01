from typing import Sequence

from coboml.util import Atom, AtomType, Statement, Paragraph

KEYWORD = 'keyword'
STRING = 'string'
WITH = 'WITH'

ESCAPES = {
    'n': '\n',
    '\\': '\\',
    't': '\t',
    'r': '\r',
}


def parse_line(line: str) -> Statement:
    out = []
    tmp = ""
    is_string = False
    escape = False
    for tmp_char in line:
        if not is_string and tmp_char.isspace():
            out.append(Atom(AtomType.KEYWORD, tmp.upper()))
            tmp = ""
            continue
        elif is_string:
            if escape:
                if tmp_char in ESCAPES:
                    tmp += ESCAPES[tmp_char]
                    escape = False
                else:
                    raise RuntimeError(f"Invalid escape char: {tmp_char}")
            elif tmp_char == '"':
                out.append(Atom(AtomType.String, tmp))
                out.append({'type': STRING, 'value': tmp})
                is_string = False
                tmp = ""
                continue
        tmp += tmp_char
    return Statement(out)


def parse(src: str) -> Sequence[Paragraph]:

    out = []
    paragraph = []
    for line in src.splitlines():
        if line.startswith('\t'):
            if len(paragraph) > 0:
                out.append(Paragraph(paragraph))
                paragraph = []

        paragraph.append(parse_line(line))
    if len(paragraph) > 0:
        out.append(Paragraph(paragraph))
    return tuple(out)
