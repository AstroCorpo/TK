import sys
from math import factorial

from scanner import Scanner

from sly import Parser

class Mparser(Parser):

    tokens = Scanner.tokens

    # debugfile = 'parser.out'

    # Grammar rules and actions
    @_('expr "+" term')
    def expr(self, p):
        return p.expr + p.term

    @_('expr "-" term')
    def expr(self, p):
        return p.expr - p.term

    @_('term')
    def expr(self, p):
        return p.term

    @_('term "*" factor')
    def term(self, p):
        return p.term * p.factor

    @_('term "/" factor')
    def term(self, p):
        return p.term / p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('INTNUM')
    def factor(self, p):
        return p.NUMBER

    @_('"(" expr ")"')
    def factor(self, p):
        return p.expr

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "/home/piotr/TK/lab2/example1.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    parser.parse(lexer.tokenize(text))