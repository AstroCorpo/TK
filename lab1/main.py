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
        self.lineno += len(t.value)  # Śledzenie liczby linii

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(ID)
    def ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')  # Sprawdza, czy identyfikator jest w zarezerwowanych słowach
        return t

    STRING = r'"[^"]*"'

    # Definicja stringów w cudzysłowach
    @_(STRING)
    def STRING(self, t):
        t.value = t.value[1:-1]  # Usuwamy cudzysłowy z wartości stringa
        return t

    FLOATNUM = r'([0-9]+\.[0-9]*|\.[0-9]+)'
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

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "lab1/example_full.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print("(" + str(tok.lineno) + ")" + ": " + tok.type + "(" + tok.value + ")")