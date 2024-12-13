from scanner import Scanner
from parser import Mparser
import sys


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "/home/piotr/TK/lab2/example3.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    tokens = lexer.tokenize(text)


    # for tok in tokens:
    #     print("(" + str(tok.lineno) + ")" + ": " + tok.type + "(" + tok.value + ")")

    parser.parse(tokens)