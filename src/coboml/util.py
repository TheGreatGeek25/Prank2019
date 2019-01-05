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


class Modifier:
    pass


class Statement:

    def __init__(self, parsed_command: Sequence[Atom], modifiers: Sequence[Modifier] = None):
        self.atoms = tuple(parsed_command)
        self.modifiers = modifiers if modifiers is not None else ()

    def get_atoms(self):
        return self.atoms


class Paragraph:

    def __init__(self, statements: Sequence[Statement], modifiers: Sequence[Modifier] = None):
        self.statements = tuple(statements)
        self.modifiers = modifiers if modifiers is not None else ()

    def get_statements(self) -> Sequence[Statement]:
        return self.statements
