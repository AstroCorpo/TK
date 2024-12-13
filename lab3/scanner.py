from sly import Lexer

class Scanner(Lexer):
    # Reserved words
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

    # Token list
    tokens = [
        "ID", "DOTADD", "DOTSUB", "DOTMUL", "DOTDIV",
        "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN",
        "EQUAL", "NOTEQUAL", "LESSOREQUAL", "GREATEROREQUAL",
        "INTNUM", "FLOATNUM", "STRING", "TRANSPOSE",
        "PLUS", "MINUS", "MULTIPLY", "DIVIDE",
        "EQUALS", "LESS_THAN", "GREATER_THAN",
        "LPAREN", "RPAREN", "LBRACKET", "RBRACKET",
        "LBRACE", "RBRACE", "COLON", "COMMA",
        "SEMICOLON", "QUOTE"
    ] + list(reserved.values())

    # Ignored patterns
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Track newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Reserved Words and Identifiers
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(ID)
    def ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')  # Check if ID is a reserved word
        return t

    # String literals
    STRING = r'"[^"]*"'

    @_(STRING)
    def STRING(self, t):
        t.value = t.value[1:-1]  # Remove surrounding quotes
        for chr in t.value:
            if chr == "\n":
                self.lineno += 1
        return t

    # Numbers
    FLOATNUM = r'([0-9]+\.[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?'
    INTNUM = r'[0-9]+'

    # Operators and special tokens
    ADDASSIGN = r'\+\='
    DOTADD = r'\.\+'
    SUBASSIGN = r'\-\='
    DOTSUB = r'\.\-'
    DOTMUL = r'\.\*'
    MULASSIGN = r'\*\='
    DOTDIV = r'\.\/'
    DIVASSIGN = r'\/\='
    EQUAL = r'=='
    NOTEQUAL = r'!='
    LESSOREQUAL = r'<='
    GREATEROREQUAL = r'>='
    TRANSPOSE = r'\''

    # Single-character tokens as named tokens
    PLUS = r'\+'
    MINUS = r'-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    EQUALS = r'='
    LESS_THAN = r'<'
    GREATER_THAN = r'>'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COLON = r':'
    COMMA = r','
    SEMICOLON = r';'
    QUOTE = r'"'



    # Error handling
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1