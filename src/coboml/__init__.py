import coboml.parser as parser
import coboml.compiler as compiler
import coboml.util as util


def compile_file(source_file, output_file):  # Side effects :(
    output_file.write(compiler.compile_COBOML(source_file.read()))


def compile_str(source: str) -> str:
    return compiler.compile_COBOML(source)
