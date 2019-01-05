import coboml.parser as parser
from coboml.util import Statement, Paragraph, AtomType

from typing import Sequence


def compile_COBOML(src: str) -> str:
    return compile_parsed_COBOML(parser.parse(src))


def compile_parsed_COBOML(parsed: Sequence[Paragraph]) -> str:
    pass


def _compile_paragraph_step1(code: Sequence[Paragraph]) -> Sequence[Paragraph]:
    pass


def _is_step1_complete(code: Sequence[Paragraph]) -> bool:
    for paragraph in code:
        for command in paragraph.get_statements():
            if command.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                    and command.get_atoms()[0].get_value() == parser.WITH:
                return False
    return True
