#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'


#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self): #representation
        result = f'{self.error_name}: {self.details}'
        return result


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)


#######################################
# TOKENS
#######################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS' # Token_Type
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = -1
        self.current_char = None #tracking the char
        self.advance() #it will increment and start from zero

    def advance(self): # advance to the next character
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        # set the character at that position inside text / if position is less than length of the text/ when we reach the end of the text set NONE

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t': #checking whether its space or tab
                self.advance() #if YES advance to next character
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                char = self.current_char
                self.advance()                #EROR
                return [], IllegalCharError("'" + char + "'")

        return tokens, None # NONE FOR THE ERROR

    def make_number(self):
        num_str = '' #tracking number in string form
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break # float has only one dot
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char # if not dot its number
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

#######################################
# NODES
#######################################
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class  BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node, self.op_tok, self.right_node})'

#######################################
# PARSER
#######################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

##############################################################################

    def parse(self):
        res = self.expr()
        return res

    def factor(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()

        return NumberNode(tok)

    def term(self):
        return  self.bin_op(self.factor,(TT_MUL, TT_DIV))

    def expr(self):
        return  self.bin_op(self.term,(TT_PLUS, TT_MINUS))


    def bin_op(self, func, ops):
        left = func()  # Call the function
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()  # Call the function
            left = BinOpNode(left, op_tok, right)
        return left




#######################################
# RUN
#######################################

def run(text):
    lexer = Lexer(text) #create new lexer
    tokens, error = lexer.make_tokens() #pass new tokens
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()


    return ast, None #tokens, error