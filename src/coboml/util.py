from typing import Sequence
from enum import Enum, auto


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
        return self.get_value()

    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.atom_type == other.get_atom_type() and self.value == other.get_value()


class Statement:

    def __init__(self, parsed_command: Sequence[Atom]):
        self._statement = parsed_command


class Paragraph:

    def __init__(self, statements: Sequence[Statement]):
        self.statements = tuple(statements)

    def get_statements(self) -> Sequence[Statement]:
        return self.statements
s