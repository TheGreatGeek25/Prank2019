KEYWORD = 'keyword'
STRING = 'string'

ESCAPES = {
    'n': '\n',
    '\\': '\\',
    't': '\t',
    'r': '\r',
}


def parse_line(line: str) -> list:
    out = []
    tmp = ""
    is_string = False
    escape = False
    for tmp_char in line:
        if not is_string and tmp_char.isspace():
            out.append({'type': KEYWORD, 'value': tmp})
            tmp = ""
            continue
        elif is_string:
            if escape:
                if tmp_char in ESCAPES:
                    tmp += ESCAPES[tmp_char]
                    escape = False
                else:
                    raise RuntimeError(f"Invalid escape char: {tmp_char}")
            elif tmp_char == '"':
                out.append({'type': STRING, 'value': tmp})
                is_string = False
                tmp = ""
                continue
        tmp += tmp_char
    return out


def parse(src: str) -> tuple:
    return tuple(map(parse_line, src.splitlines()))
