from scanner import Scanner
from parser import Mparser
from printer import TreePrinter
import sys

if __name__ == "__main__":

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "/home/piotr/TK/lab3/example1.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))

    ast.printTree()