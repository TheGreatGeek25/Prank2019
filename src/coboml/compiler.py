import coboml.parser as parser
from coboml.util import Statement, Paragraph, AtomType

from typing import Sequence, Dict, Callable, Any
import re


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


TEXT_PATTERN = ((AtomType.KEYWORD, "ADD"), (AtomType.KEYWORD, "TEXT"), (AtomType.KEYWORD, re.compile("(?s).*")))
IMAGE_PATTERN = ((AtomType.KEYWORD, "ADD"), (AtomType.KEYWORD, "IMAGE"),
                 (AtomType.KEYWORD, "FROM"), (AtomType.STRING, re.compile(".*")))  # TODO: Validate URIs


def compile_COBOML(src: str) -> str:
    return compile_parsed_COBOML(parser.parse(src))


def compile_parsed_COBOML(parsed: Sequence[Paragraph]) -> str:
    pass


def _compile1_next_statement_with_mods(statements: Sequence[Statement]) -> (IFElement, int):
    """Returns the IFElements and the number of statements read"""
    main_statement = statements[0]

    if main_statement.matches_pattern(TEXT_PATTERN):
        ifelement = IFText(main_statement.get_atoms()[2].get_value())
    elif main_statement.matches_pattern(IMAGE_PATTERN):
        raise NotImplementedError("Images have not been implemented yet")  # FIXME: Implement images
    else:
        raise ValueError("Unknown statement")

    mods = []
    for statement in statements[1:]:
        if statement.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                and statement.get_atoms()[0].get_value() == parser.WITH:
            mods.append(statement)
        else:
            break

    for mod in mods:
        build_modifier(mod).get_fun()(ifelement)  # Uses side effects :(

    return ifelement, len(mods) + 1


def _compile1_paragraph(paragraph: Paragraph) -> IFParagraph:
    statements = paragraph.get_statements()
    paragraph_mods = []
    for statement in statements:
        if statement.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                and statement.get_atoms()[0].get_value() == parser.WITH:
            paragraph_mods.append(statement)
        else:
            break

    paragraph_statements = []
    index = len(paragraph_mods)+1
    while index < len(statements):
        tmp_statement, tmp_index = _compile1_next_statement_with_mods(statements[index:])
        paragraph_statements.append(tmp_statement)
        index += tmp_index
    ifparagraph = IFParagraph(paragraph_statements)

    for mod in paragraph_mods:
        build_modifier(mod).get_fun()(ifparagraph)  # Uses side effects :(

    return ifparagraph


def build_modifier(with_statement: Statement) -> IFModifier:
    pass


def _is_step1_complete(code: Sequence[Paragraph]) -> bool:
    for paragraph in code:
        for command in paragraph.get_statements():
            if command.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                    and command.get_atoms()[0].get_value() == parser.WITH:
                return False
    return True
