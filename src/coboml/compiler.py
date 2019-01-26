import coboml.parser as parser
from coboml.util import Statement, Paragraph, AtomType, html_escape_quotes

from typing import Sequence, Dict, Callable, Tuple, Any


class IFElement:  # TODO
    """Intermediate representation of a COBOML element"""

    def __init__(self, html: str):
        self.html = html

    def get_html(self, params: Dict[str, Any]) -> str:
        return self.html.format_map(params)

    def set_html(self, html: str):
        self.html = html


class IFParagraph(IFElement):  # TODO
    """Intermediate representation of a paragraph"""

    def __init__(self, elements: Sequence[IFElement]):
        IFElement.__init__(self, "")
        self.elements = tuple(elements)
        self.set_html("<span>{elements}</span>")
        self.params = {}

    def get_elements(self):
        return self.elements

    def set_param(self, key: str, value: str):
        self.params[key] = value

    def get_html(self, params: Dict[str, Any]):
        return self.html.format(elements=''.join(map(lambda e: e.get_html(params), self.elements))).format_map(params)


class IFText(IFElement):
    """Intermediate representation of a text element"""

    def __init__(self, text: str):
        IFElement.__init__(self, "")
        self.text = text

    def get_html(self, params: Dict[str, Any]):
        return self.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class IFImage(IFElement):  # TODO
    """Intermediate representation of an image element"""


class IFModifier:

    def __init__(self, fun: Callable[[IFElement], IFElement]):
        self.fun = fun

    def get_fun(self):
        return self.fun


class IFModifierBuilder:

    def __init__(self, builder: Callable[[Sequence], IFModifier]):
        self.builder = builder

    def __call__(self, args: Sequence):
        return self.builder(args)


def compile_COBOML(src: str) -> str:
    return compile_parsed_COBOML(parser.parse(src))


def compile_parsed_COBOML(parsed: Sequence[Paragraph]) -> str:
    pass


def _compile_paragraph(paragraph: Paragraph) -> IFParagraph:
    statements = paragraph.get_statements()
    paragraph_mods = []
    for statement in statements:
        if statement.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                and statement.get_atoms()[0].get_value() == parser.WITH:
            paragraph_mods.append(statement)
        else:
            break

    # TODO


def build_modifier(with_statement: Statement) -> IFModifier:
    pass


def _is_step1_complete(code: Sequence[Paragraph]) -> bool:
    for paragraph in code:
        for command in paragraph.get_statements():
            if command.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                    and command.get_atoms()[0].get_value() == parser.WITH:
                return False
    return True
