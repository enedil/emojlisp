import sys

from error import error
import lexer
import parse
import interpreter

if __name__ == '__main__':

    if len(sys.argv) == 1:
        src = input()
    else:
        src = open(sys.argv[1]).read()

    # print(type(lexem('(', 2, 0)))
    # print(emojify(lexer(texxxxxt)))
    print(interpreter.run(parse.parse(lexer.lexer(src))))