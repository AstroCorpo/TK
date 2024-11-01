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

    tokens = ["ID", "DOTADD", "DOTSUB", "DOTMUL", "DOTDIV", "TRANSPOSE", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN", "EQUAL", 'NOTEQUAL', 'LESSOREQUAL', 'GREATEROREQUAL', "INTNUM", 'FLOATNUM', 'STRING'] + list(reserved.values())

    @_(r' ')
    def ignore_space(self, t):
        pass

    @_(r'\t')
    def ignore_tab(self, t):
        pass

    @_(r'\#.*')
    def ignore_comment(self, t):
        pass

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')
        return t

    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        self.lineno += t.value.count('\n')
        return t

    FLOATNUM = r'([0-9]+\.[0-9]*|\.[0-9]+|[0-9]+\.[0-9]*[eE][+-]?[0-9]+|[0-9]+[eE][+-]?[0-9]+)'

    INTNUM = r'[0-9]+'

    DOTADD = r'\.\+'

    DOTSUB = r'\.\-'

    DOTMUL = r'\.\*'

    DOTDIV = r'\.\/'

    TRANSPOSE = '\''

    ADDASSIGN = r'\+\='

    SUBASSIGN = r'\-\='

    MULASSIGN = r'\*\='

    DIVASSIGN = r'\/\='

    LESSOREQUAL = r'<='

    GREATEROREQUAL = r'>='

    EQUAL = r'=='

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "/home/piotr/TK/lab1/example_full.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print("(" + str(tok.lineno) + ")" + ": " + tok.type + "(" + tok.value + ")")