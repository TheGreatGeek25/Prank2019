import coboml.parser as parser
from coboml.util import Statement

from typing import Sequence


def compile_COBOML(src: str) -> str:
    return compile_parsed_COBOML(parser.parse(src))


def compile_parsed_COBOML(parsed: Sequence[Statement]) -> str:
    pass


def _compile_step1(code: Sequence[Statement]) -> Sequence[Statement]:
    pass


def _get_first_with(code: Sequence[Statement]):
    pass


def _is_step1_complete(code: Sequence[Statement]) -> bool:
    for command in code:
        if command['type'] == parser.KEYWORD and command['value'] == parser.WITH:
            return False
    return True
