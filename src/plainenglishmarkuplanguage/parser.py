# Copyright 2019 TheGreatGeek
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Sequence

from plainenglishmarkuplanguage.util import Atom, AtomType, Statement, Paragraph

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
                    continue
                else:
                    raise RuntimeError(f"Invalid escape char: {tmp_char}")
            elif tmp_char == '"':
                out.append(Atom(AtomType.STRING, tmp))
                is_string = False
                tmp = ""
                continue
            elif tmp_char == '\\':
                escape = True
                continue
        elif tmp == "" and tmp_char == '"':
            is_string = True
            continue
        tmp += tmp_char
    if tmp != "" and not is_string:
        out.append(Atom(AtomType.KEYWORD, tmp.upper()))
    return Statement(out)


def parse(src: str) -> Sequence[Paragraph]:

    out = []
    paragraph = []
    for line in src.splitlines():
        if line.startswith('\t'):
            if len(paragraph) > 0:
                out.append(Paragraph(paragraph))
                paragraph = []
            paragraph.append(parse_line(line[1:]))
        else:
            paragraph.append(parse_line(line))
    if len(paragraph) > 0:
        out.append(Paragraph(paragraph))
    return tuple(out)
