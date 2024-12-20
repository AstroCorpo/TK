from scanner import Scanner
import sys

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