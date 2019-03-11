import re
from typing import Sequence, Callable

import coboml.parser as parser
from coboml.util import Statement, Paragraph, AtomType


class IFElement:  # TODO
    """Intermediate representation of a COBOML element"""

    def __init__(self, html: str):
        self.html = html
        self.params = {}

    def get_raw_html(self) -> str:
        return self.html

    def set_param(self, key: str, value: str):
        self.params[key] = value

    def get_html(self) -> str:
        return self.html.format_map(self.params)

    def set_html(self, html: str):
        self.html = html


class IFParagraph(IFElement):
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

    def get_html(self):
        return self.html.format(elements=''.join(map(lambda e: e.get_html(), self.elements))).format_map(self.params)


class IFText(IFElement):
    """Intermediate representation of a text element"""

    def __init__(self, text: str):
        IFElement.__init__(self, text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>'))
        self.text = text


class IFImage(IFElement):  # TODO
    """Intermediate representation of an image element"""

    def __init__(self, src: str):
        IFElement.__init__(self, f'<img src="{src}"/>')


class IFModifier:

    def __init__(self, fun: Callable[[IFElement], IFElement]):
        self.fun = fun

    def get_fun(self):
        return self.fun


class IFModifierBuilder:

    def __init__(self, builder: Callable[[Statement], IFModifier]):
        self.builder = builder

    def __call__(self, arg: Statement):
        return self.builder(arg)

# ==========================================
#              Begin Modifiers
# ==========================================


MOD_BOLD_PATTERN = ((AtomType.KEYWORD, "WITH"), (AtomType.KEYWORD, "BOLD"), (AtomType.KEYWORD, "TEXT"))
def _mod_bold_function(element: IFElement) -> IFElement:
    element.set_html(f'<b>{element.get_raw_html()}</b>')
    return element


MOD_ITALIC_PATTERN = ((AtomType.KEYWORD, "WITH"), (AtomType.KEYWORD, "ITALIC"), (AtomType.KEYWORD, "TEXT"))
def _mod_italic_function(element: IFElement) -> IFElement:
    element.set_html(f'<i>{element.get_raw_html()}</i>')
    return element


MOD_LINK_PATTERN = ((AtomType.KEYWORD, "WITH"), (AtomType.KEYWORD, "LINK"),
                    (AtomType.KEYWORD, "TO"), (AtomType.STRING, re.compile(".*")))  # TODO: Validate URIs
def _mod_link_builder_function(statement: Statement):
    def _mod_link_function(element: IFElement):
        element.set_html(f'<a href="{statement.get_atoms()[3].get_value()}">{element.get_raw_html()}</a>')
        return element
    return IFModifier(_mod_link_function)


modifiers = (
    (MOD_BOLD_PATTERN, IFModifierBuilder(lambda statement: IFModifier(_mod_bold_function))),
    (MOD_ITALIC_PATTERN, IFModifierBuilder(lambda statement: IFModifier(_mod_italic_function))),
    (MOD_LINK_PATTERN, IFModifierBuilder(_mod_link_builder_function))
)

# ==========================================
#               End Modifiers
# ==========================================

TEXT_PATTERN = ((AtomType.KEYWORD, "ADD"), (AtomType.KEYWORD, "TEXT"), (AtomType.STRING, re.compile("(?s).*")))
IMAGE_PATTERN = ((AtomType.KEYWORD, "ADD"), (AtomType.KEYWORD, "IMAGE"),
                 (AtomType.KEYWORD, "FROM"), (AtomType.STRING, re.compile(".*")))  # TODO: Validate URIs


def compile_COBOML(src: str) -> str:
    return compile_parsed_COBOML(parser.parse(src))


def compile_parsed_COBOML(parsed: Sequence[Paragraph]) -> str:
    ifparagraphs = tuple(map(_compile1_paragraph, parsed))
    header = '<html><body>'
    footer = '</body></html>'

    tmp = header
    for ifparagraph in ifparagraphs:
        tmp += ifparagraph.get_html()
    tmp += footer

    return tmp


def _compile1_next_statement_with_mods(statements: Sequence[Statement]) -> (IFElement, int):
    """Returns the IFElements and the number of statements read"""
    main_statement = statements[0]

    if main_statement.matches_pattern(TEXT_PATTERN):
        ifelement = IFText(main_statement.get_atoms()[2].get_value())
    elif main_statement.matches_pattern(IMAGE_PATTERN):
        ifelement = IFImage(main_statement.get_atoms()[3].get_value())
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
    index = len(paragraph_mods)
    while index < len(statements):
        tmp_statement, tmp_index = _compile1_next_statement_with_mods(statements[index:])
        paragraph_statements.append(tmp_statement)
        index += tmp_index
    ifparagraph = IFParagraph(paragraph_statements)

    for mod in paragraph_mods:
        build_modifier(mod).get_fun()(ifparagraph)  # Uses side effects :(

    return ifparagraph


def build_modifier(with_statement: Statement) -> IFModifier:
    for mod_pattern, mod_builder in modifiers:
        if with_statement.matches_pattern(mod_pattern):
            return mod_builder(with_statement)
    raise ValueError('Unknown modifier')


def _is_step1_complete(code: Sequence[Paragraph]) -> bool:
    for paragraph in code:
        for command in paragraph.get_statements():
            if command.get_atoms()[0].get_atom_type() == AtomType.KEYWORD \
                    and command.get_atoms()[0].get_value() == parser.WITH:
                return False
    return True
