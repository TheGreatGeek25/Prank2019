import coboml.parser as parser


def compile_COBOML(src: str) -> str:
    return compile_parsed_COBOML(parser.parse(src))


def compile_parsed_COBOML(parsed: tuple) -> str:
    pass
