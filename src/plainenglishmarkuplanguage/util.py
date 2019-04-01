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

from typing import Sequence, Dict
from enum import Enum, auto
import re


class AtomType(Enum):
    KEYWORD = auto()
    STRING = auto()


class Atom:

    def __init__(self, atom_type: AtomType, value):
        self.atom_type = atom_type
        self.value = value

    def get_atom_type(self) -> AtomType:
        return self.atom_type

    def get_value(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.atom_type == other.get_atom_type() and self.value == other.get_value()

    def __str__(self):
        return f"Atom({self.atom_type}, {self.value})"


class Statement:

    def __init__(self, parsed_command: Sequence[Atom]):
        self.atoms = tuple(parsed_command)

    def get_atoms(self) -> Sequence[Atom]:
        return self.atoms

    def matches_pattern(self, pattern) -> bool:
        atoms = self.get_atoms()
        if len(atoms) != len(pattern):
            return False
        for i, pattern_part in enumerate(pattern):
            if pattern_part[0] == AtomType.KEYWORD and atoms[i].get_atom_type() == AtomType.KEYWORD:
                if atoms[i].get_value() != pattern_part[1]:
                    return False
            elif pattern_part[0] == AtomType.STRING and atoms[i].get_atom_type() == AtomType.STRING:
                if pattern_part[1].fullmatch(atoms[i].get_value()) is None:
                    return False
        return True

    def __str__(self):
        return str(tuple(map(str, self.atoms)))


class Paragraph:

    def __init__(self, statements: Sequence[Statement]):
        self.statements = tuple(statements)

    def get_statements(self) -> Sequence[Statement]:
        return self.statements


def html_escape_quotes(html: str) -> str:
    return html.replace('"', '&quot;').replace("'", '&#39;')


def str_tag_params(tag_params: Dict[str, str]) -> str:
    return ' '.join(map(lambda kv: '"{}"="{}"'.format(*map(html_escape_quotes, kv)), tag_params.items()))


class FormatDict(dict):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            return "{" + str(item) + "}"
