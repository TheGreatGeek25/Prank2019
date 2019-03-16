import coboml

from sys import argv, stdin, stderr

if len(argv) > 1:
    for file_name in argv[1:]:
        source_file = open(file_name, 'r')
        output_file = open(f'{file_name}.html', 'w')
        coboml.compile_file(source_file, output_file)
        source_file.close()
        output_file.close()
else:
    print("No arguments: reading from STDIN", file=stderr)
    print(coboml.compile_str(stdin.read()))
