from sly import Parser
from scanner import Scanner
import AST
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
debug_path = os.path.join(SCRIPT_PATH, "parser.out")


class Mparser(Parser):
    tokens = Scanner.tokens

    debugfile = debug_path

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'EQUAL', 'NOTEQUAL'),
        ("nonassoc", 'LESS_THAN', 'GREATER_THAN', 'LESSOREQUAL', 'GREATEROREQUAL'),
        ("left", 'PLUS', 'MINUS', 'DOTADD', 'DOTSUB'),
        ("left", 'MULTIPLY', 'DIVIDE', 'DOTMUL', 'DOTDIV'),
        ("right", 'UMINUS'),
    )

    def __init__(self):
        super().__init__()
        self.variables = {}

    @_('instructions')  # type: ignore
    def instructions_opt(self, p):
        return AST.CompoundStatement(instructions=p.instructions, line = p.lineno)

    @_('')  # type: ignore
    def instructions_opt(self, p):
        return []

    @_('instructions instruction')  # type: ignore
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction')  # type: ignore
    def instructions(self, p):
        return [p.instruction]

    @_('PRINT elements SEMICOLON')  # type: ignore
    def instruction(self, p):
        return AST.PrintInstruction(value=p.elements, line=p.lineno)

    @_('RETURN expr SEMICOLON')  # type: ignore
    def instruction(self, p):
        return AST.ReturnInstruction(value=p.expr, line=p.lineno)

    @_('BREAK SEMICOLON',  # type: ignore
       'CONTINUE SEMICOLON')
    def instruction(self, p):
        val = p[0].upper()
        if val == 'BREAK':
            return AST.BreakInstruction(value=p[0], line=p.lineno)
        elif val == 'CONTINUE':
            return AST.ContinueInstruction(value=p[0], line=p.lineno)

    @_('LBRACE instructions RBRACE')  # type: ignore
    def instruction(self, p):
        return p.instructions

    @_('IF LPAREN expr RPAREN instruction %prec IFX')  # type: ignore
    def instruction(self, p):
        return AST.ConditionalInstruction(condition=p.expr, instructions=p.instruction, else_instruction=None, line=p.lineno)

    @_('IF LPAREN expr RPAREN instruction ELSE instruction')  # type: ignore
    def instruction(self, p):
        return AST.ConditionalInstruction(condition=p.expr, instructions=p.instruction0, else_instruction=p.instruction1, line=p.lineno)

    @_('WHILE LPAREN expr RPAREN instruction')  # type: ignore
    def instruction(self, p):
        return AST.WhileLoop(condition=p.expr, instructions=p.instruction, line=p.lineno)

    @_('FOR ID EQUALS expr COLON expr instruction')  # type: ignore
    def instruction(self, p):
        return AST.ForLoop(id=p.ID, range=AST.Range(start=p.expr0, end=p.expr1), instructions=p.instruction, line=p.lineno)

    @_('assignment SEMICOLON')  # type: ignore
    def instruction(self, p):
        return p.assignment

    @_('ID assign expr')  # type: ignore
    def assignment(self, p):
        return AST.Assignment(id=p.ID, assign_type=p.assign, value=p.expr, line=p.lineno)

    @_('ID LBRACKET elements RBRACKET assign expr')  # type: ignore
    def assignment(self, p):
        return AST.AssignIndex(id=p.ID, index=p.elements, assign_type=p.assign, value=p.expr, line=p.lineno)

    @_('ID LBRACKET elements RBRACKET')  # type: ignore
    def expr(self, p):
        return AST.ArrayAccess(p[0], p[2], line=p.lineno)

    @_('EQUALS',  # type: ignore
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign(self, p):
        return p[0]

    @_('expr EQUAL expr',  # type: ignore
       'expr NOTEQUAL expr',
       'expr LESS_THAN expr',
       'expr GREATER_THAN expr',
       'expr LESSOREQUAL expr',
       'expr GREATEROREQUAL expr')
    def expr(self, p):
        return AST.RelationExpr(op=p[1], left=p.expr0, right=p.expr1, line=p.lineno)

    @_('expr PLUS expr',  # type: ignore
       'expr MINUS expr',
       'expr MULTIPLY expr',
       'expr DIVIDE expr')
    def expr(self, p):
        return AST.BinExpr(op=p[1], left=p.expr0, right=p.expr1, line=p.lineno)

    @_('expr DOTADD expr',  # type: ignore
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(op=p[1], left=p.expr0, right=p.expr1, line=p.lineno)

    @_('LPAREN expr RPAREN')  # type: ignore
    def expr(self, p):
        return p.expr

    @_('INTNUM')  # type: ignore
    def expr(self, p):
        return AST.IntNum(value=p.INTNUM, line=p.lineno)

    @_('FLOATNUM')  # type: ignore
    def expr(self, p):
        return AST.FloatNum(value=p.FLOATNUM, line=p.lineno)

    @_('STRING')  # type: ignore
    def expr(self, p):
        return AST.String(value=p.STRING, line=p.lineno)

    @_('ID')  # type: ignore
    def expr(self, p):
        return AST.Variable(name=p.ID, line=p.lineno)

    @_('EYE LPAREN elements RPAREN',  # type: ignore
       'ZEROS LPAREN elements RPAREN',
       'ONES LPAREN elements RPAREN')
    def expr(self, p):
        return AST.MatrixFunction(name=p[0], params=p.elements, line=p.lineno)

    @_('MINUS expr %prec UMINUS')  # type: ignore
    def expr(self, p):
        return AST.UnaryExpr(op='-', value=p.expr, line=p.lineno)

    @_('vector')  # type: ignore
    def expr(self, p):
        return p.vector

    @_('LBRACKET elements RBRACKET')  # type: ignore
    def vector(self, p):
        return AST.Vector(elements=p.elements, line=p.lineno)

    @_('expr COMMA elements')  # type: ignore
    def elements(self, p):
        return [p.expr] + p.elements

    @_('expr')  # type: ignore
    def elements(self, p):
        return [p.expr]

    @_('expr TRANSPOSE')  # type: ignore
    def expr(self, p):
        return AST.Transpose(value=p.expr, line=p.lineno)
