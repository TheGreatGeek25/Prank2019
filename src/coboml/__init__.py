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

import coboml.parser as parser
import coboml.compiler as compiler
import coboml.util as util

from sys import argv, stderr


def compile_file(source_file, output_file):
    output_file.write(compiler.compile_COBOML(source_file.read()))


def compile_str(source: str) -> str:
    return compiler.compile_COBOML(source)


def main():
    if len(argv) == 2:
        source_file = open(argv[1], 'r')
        output_file = open(f'{argv[1]}.html', 'w')
        compile_file(source_file, output_file)
        source_file.close()
        output_file.close()
    elif len(argv) == 3:
        source_file = open(argv[1], 'r')
        output_file = open(argv[2], 'w')
        compile_file(source_file, output_file)
        source_file.close()
        output_file.close()
    else:
        print("Missing arguments", file=stderr)
        print('Usage: coboml <source-file> [output-file]')
