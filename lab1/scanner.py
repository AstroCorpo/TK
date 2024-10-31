import sys

from sly import Lexer

class Scanner(Lexer):

    literals = ['+',
                '-',
                '*',
                '/',
                '=',
                '<',
                '>',
                '(',
                ')',
                '[',
                ']',
                '{',
                '}',
                ':',
                '\'',
                ',',
                ';',
                '"']

    reserved = {'if': 'IF',
                'else': 'ELSE',
                'for': 'FOR',
                'while': 'WHILE',
                'break': 'BREAK',
                'continue': 'CONTINUE',
                'return': 'RETURN',
                'eye': 'EYE',
                'zeros': 'ZEROS',
                'ones': 'ONES',
                'print': 'PRINT'}

    tokens = ["ID", "DOTADD", "DOTSUB", "DOTMUL", "DOTDIV", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN", "EQUAL", 'NOTEQUAL', 'LESSOREQUAL', 'GREATEROREQUAL', "INTNUM", 'FLOATNUM', 'STRING'] + list(reserved.values())

    ignore = ' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(ID)
    def ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')
        return t

    STRING = r'"[^"]*"'

    @_(STRING)
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    FLOATNUM = r'([0-9]+\.[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?'

    INTNUM = r'\b[0-9]+\b(?!\.[0-9]+)'

    DOTADD = r'\.\+'

    SUBASSIGN = r'\-\='

    DOTSUB = r'\.\-'

    DOTMUL = r'\.\*'

    MULASSIGN = r'\*\='

    DOTDIV = r'\.\/'

    DIVASSIGN = r'\/\='

    LESSOREQUAL = r'<='

    GREATEROREQUAL = r'>='

    EQUAL = r'=='
