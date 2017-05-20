from error import *


class Node:
    def __init__(self, lexem):
        self.kids = []
        self.token = lexem

    def adopt(self, kid):
        self.kids.append(kid)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return str(self)

    def _to_string(self, depth=0):
        return '  ' * depth + '\n'.join([str(self.token)] + [k._to_string(depth+1) for k in self.kids])



def parens(lexems, offset, typee):
    i = offset + 1
    l = Node(lexems[offset])
    while not lexems[i][0] == typee:
        c, i = parsε(lexems, i)
        l.adopt(c)

    return l, i + 1


def apply_form(lexems, offset):
    return parens(lexems, offset, ')')


def vector_form(lexems, offset):
    return parens(lexems, offset, ']')


def assoc_form(lexems, offset):
    iiiiii, jjjjjj = parens(lexems, offset, '}')
    if len(iiiiii.kids) % 2 == 1:
        error(SyntaxError, 'Odd number of elems in assoc table')
    return iiiiii, jjjjjj




def shallowy(lexem, offset):
    return Node(lexem[offset]), offset + 1

type_map = {
    'symbol': shallowy,
    'number': shallowy,
    'string': shallowy,
    '(': apply_form,
    '[': vector_form,
    '{': assoc_form
}

def parsε(lexems, offset):
    global type_map

    try:
        return type_map[lexems[offset][0]](lexems, offset)
    except:
        error(SyntaxError, 'ZŁe nawjasy {}'.format(lexems[offset]))


def parse(lexems):
    root = Node(['root','root',0,0])
    i = 0
    while i < len(lexems):
        c, i = parsε(lexems, i)
        root.adopt(c)
    return root



































