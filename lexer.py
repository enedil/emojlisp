import parse
from error import error


map = {
        '👍': '(',
        '👎': ')',
        '👍🏽': '[',
        '👎🏽': ']',
        '👍🏿': '{',
        '👎🏿': '}',
        '👍🏻': '<',
        '👎🏻': '>',
        '📍': '.',
        '👀': ';',
        '🍏': '+',
        '🍓': '-',
        '🍒': '*',
        '🍆': '/',
        '✨': '√',
        '(': '🐅',
        ')': '🐃',
        '[': '🐂',
        ']': '🐄',
        '{': '🐪',
        '}': '🐫'
    }

def demojify(text):
    global map

    #print(text)

    if len(text) == 0:
        return ''
    try:
        return map[text[0]] + demojify(text[1:])
    except KeyError:
        reversemap = {v: k for k, v in map.items()}
        try:
            reversemap[text[0]]
        except:
            return text[0] + demojify(text[1:])
        #finally:
        #    error(SyntaxError, 'jesteś złym człowiekiem')



def emojify(text):
    global map

    reversemap = {v: k for k, v in map.items()}

    if len(text) == 0:
        return ''
    try:
        return reversemap[text[0]] + emojify(text[1:])
    except KeyError:
        return text[0] + emojify(text[1:])

def type_id(text):
    fixed = {e: e for e in '(){}[]'}
    try:
        fixed[text]
        return text
    except KeyError:
        if text[0] == '"':
            if text[-1] != '"':
                raise SyntaxError()
            else:
                return 'string'
        try:
            float(text)
            return 'number'
        except ValueError:
            return 'symbol'


def lexem(text, line, col):
    try:
        # print('Lexer here 😱 : ', text)
        return (type_id(text), text, line, col, )
    except SyntaxError:
        bład = 'Unterminated string at line {} and column {}'
        raise SyntaxError(bład.format(line, col))


def lexer(text):
    text = demojify(text)
    lines = text.splitlines()
    lexems = []
    for iline, line in enumerate(lines):
        pos = 0
        is_str = False
        for ichar, char in enumerate(line):
            if is_str:
                if char == '"':
                    lexems.append(lexem(line[pos:ichar+1], iline, ichar))
                    pos = ichar + 1
                    is_str = False
            elif char == ';':
                pos = len(line)
                break

            elif char in ' \t':
                if pos != ichar:
                    lexems.append(lexem(line[pos:ichar], iline, ichar))
                pos = ichar + 1

            elif char in '(){}[]':
                if pos != ichar:
                    lexems.append(lexem(line[pos:ichar], iline, ichar))
                lexems.append(lexem(char, iline, ichar))
                pos = ichar + 1

            elif char == '"':
                if pos != ichar:
                    lexems.append(lexem(line[pos:ichar], iline, ichar))
                    pos = ichar
                is_str = True

        if pos != len(line):
            lexems.append(lexem(line[pos:], iline, ichar))

    return lexems
