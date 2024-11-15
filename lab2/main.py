import sys

from scanner import Scanner

from sly import Parser
class Mparser(Parser):

    tokens = Scanner.tokens

    precedence = (
        ('left', '+', '-', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
        ('right', '\''),
        ('right', 'UMINUS'),
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
    )

    @_('statement_list')
    def program(self, p):
        pass

    @_('statement_list statement')
    def statement_list(self, p):
        pass

    @_('statement')
    def statement_list(self, p):
        pass

    @_('assignment_statement',
       'print_statement',
       'if_statement',
       'while_statement',
       'for_statement',
       'break_statement',
       'continue_statement',
       'return_statement')
    def statement(self, p):
        pass

    @_('ID "[" INTNUM "," INTNUM "]" "=" expr ";"')
    def matrix_element_assignment(self, p):
        pass

    @_('"[" matrix_rows "]"')
    def matrix_value_initialization(self, p):
        pass

    @_('matrix_rows "," matrix_row')
    def matrix_rows(self, p):
        pass

    @_('matrix_row')
    def matrix_rows(self, p):
        pass

    @_('"[" expr_list "]"')
    def matrix_row(self, p):
        pass

    @_('EYE "(" INTNUM ")"')
    def matrix_func_initialization(self, p):
        pass

    @_('ZEROS "(" INTNUM ")"')
    def matrix_func_initialization(self, p):
        pass

    @_('ONES "(" INTNUM ")"')
    def matrix_func_initialization(self, p):
        pass

    @_('matrix_value_initialization',
       'matrix_func_initialization')
    def matrix_init(self, p):
        pass

    @_('ID "=" expr ";"')
    def assignment_expr_statement(self, p):
        pass

    @_('ID "=" matrix_expr ";"')
    def assignment_matrix_expr_statement(self, p):
        pass

    @_('expr ADDASSIGN expr ";"',
       'expr SUBASSIGN expr ";"',
       'expr MULASSIGN expr ";"',
       'expr DIVASSIGN expr ";"')
    def assignment_with_operation(self, p):
        pass

    @_('assignment_expr_statement',
       'assignment_matrix_expr_statement',
       'assignment_with_operation',
       'matrix_element_assignment')
    def assignment_statement(self, p):
        pass

    @_('PRINT STRING ";"')
    def print_statement(self, p):
        pass

    @_('PRINT expr_list ";"')
    def print_statement(self, p):
        pass

    @_('IF "(" condition ")" statement_list %prec IFX',
       'IF "(" condition ")" statement_list ELSE statement_list',
       'IF "(" condition ")" "{" statement_list "}" %prec IFX',
       'IF "(" condition ")" "{" statement_list "}" ELSE statement_list')
    def if_statement(self, p):
        pass

    @_('WHILE "(" condition ")" statement_list',
       'WHILE "(" condition ")" "{" statement_list "}"')
    def while_statement(self, p):
        pass

    @_('FOR ID "=" expr ":" expr statement_list',
       'FOR ID "=" expr ":" expr "{" statement_list "}"')
    def for_statement(self, p):
        pass

    @_('BREAK ";"')
    def break_statement(self, p):
        pass

    @_('CONTINUE ";"')
    def continue_statement(self, p):
        pass

    @_('RETURN expr ";"')
    def return_statement(self, p):
        pass

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        pass

    @_('ID', 'INTNUM', 'FLOATNUM')
    def expr(self, p):
        pass

    @_('"(" expr ")"')
    def expr(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('neg', p.expr)

    @_('expr_list "," expr')
    def expr_list(self, p):
        pass

    @_('expr')
    def expr_list(self, p):
        pass

    @_('matrix_init')
    def matrix_expr(self, p):
        pass

    @_('matrix_expr DOTADD matrix_expr',
       'matrix_expr DOTSUB matrix_expr',
       'matrix_expr DOTMUL matrix_expr',
       'matrix_expr DOTDIV matrix_expr',)
    def matrix_expr(self, p):
        pass

    @_('matrix_expr "\'"')
    def matrix_expr(self, p):
        pass

    @_('expr EQUAL expr',
       'expr NOTEQUAL expr',
       'expr LESSOREQUAL expr',
       'expr GREATEROREQUAL expr',
       'expr "<" expr',
       'expr ">" expr')
    def condition(self, p):
        pass

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
