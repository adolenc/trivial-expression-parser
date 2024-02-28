### Lexer part
class Token:
    def __init__(self, type, value):
        self.type, self.value = type, value

TOKEN_TYPE_PLUS = 0
TOKEN_TYPE_MINUS = 1
TOKEN_TYPE_STAR = 2
TOKEN_TYPE_SLASH = 3
TOKEN_TYPE_CARET = 4
TOKEN_TYPE_EXCLAMATION = 5
TOKEN_TYPE_OPEN_PAREN = 6
TOKEN_TYPE_CLOSE_PAREN = 7
TOKEN_TYPE_NUMBER = 8
TOKEN_TYPE_EOF = 9

def tokenize(expr):
    def convert_to_token(c):
        char_to_token_type = {
            '+': TOKEN_TYPE_PLUS,
            '-': TOKEN_TYPE_MINUS,
            '*': TOKEN_TYPE_STAR,
            '/': TOKEN_TYPE_SLASH,
            '^': TOKEN_TYPE_CARET,
            '!': TOKEN_TYPE_EXCLAMATION,
            '(': TOKEN_TYPE_OPEN_PAREN,
            ')': TOKEN_TYPE_CLOSE_PAREN
        }
        if c in char_to_token_type:
            return Token(char_to_token_type[c], c)
        elif c[0].isdigit():
            return Token(TOKEN_TYPE_NUMBER, int(c))
        else:
            raise Exception(f'Unknown token: {c}')

    return [convert_to_token(c) for c in expr.split(' ')] \
         + [Token(TOKEN_TYPE_EOF, None)]


### Parser part
class NumberExpression:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f'{self.value}'

class UnaryExpression:
    def __init__(self, operator, expr):
        self.operator, self.expr = operator, expr
    def __str__(self):
        return f'({self.operator} {self.expr})'

class BinaryExpression:
    def __init__(self, left_expr, operator, right_expr):
        self.left_expr, self.operator, self.right_expr = left_expr, operator, right_expr
    def __str__(self):
        return f'({self.operator} {self.left_expr} {self.right_expr})'

PRECEDENCE_MIN = 0 
PRECEDENCE_SUM = 1
PRECEDENCE_PRODUCT = 2
PRECEDENCE_EXPONENT = 3
PRECEDENCE_PREFIX = 4
PRECEDENCE_POSTFIX = 5

ASSOCIATIVITY_LEFT = 0
ASSOCIATIVITY_RIGHT = 1

class ParseRule:
    def __init__(self, precedence=PRECEDENCE_MIN, associativity=ASSOCIATIVITY_LEFT):
        self.precedence, self.associativity = precedence, associativity

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.prefix_parse_rules = {
            TOKEN_TYPE_NUMBER:     ParseRule(PRECEDENCE_PREFIX),
            TOKEN_TYPE_MINUS:      ParseRule(PRECEDENCE_PREFIX),
            TOKEN_TYPE_OPEN_PAREN: ParseRule(PRECEDENCE_PREFIX),
        }
        self.infix_parse_rules = {
            TOKEN_TYPE_PLUS:        ParseRule(PRECEDENCE_SUM),
            TOKEN_TYPE_MINUS:       ParseRule(PRECEDENCE_SUM),
            TOKEN_TYPE_STAR:        ParseRule(PRECEDENCE_PRODUCT),
            TOKEN_TYPE_SLASH:       ParseRule(PRECEDENCE_PRODUCT),
            TOKEN_TYPE_CARET:       ParseRule(PRECEDENCE_EXPONENT, ASSOCIATIVITY_RIGHT),
            TOKEN_TYPE_EXCLAMATION: ParseRule(PRECEDENCE_POSTFIX),
        }

    def parse(self, precedence=PRECEDENCE_MIN):
        if self.peek().type not in self.prefix_parse_rules:
            raise Exception(f'Could not parse prefix {self.peek()}')
        left_expr = self.parse_prefix(token=self.consume())
        while self.peek().type in self.infix_parse_rules and precedence < self.infix_parse_rules[self.peek().type].precedence:
            left_expr = self.parse_infix(left_expr, token=self.consume())
        return left_expr

    def parse_prefix(self, token):
        # token.type is gonna be exactly one of the keys in prefix_parse_rules
        if token.type == TOKEN_TYPE_NUMBER:
            return NumberExpression(token.value)
        elif token.type == TOKEN_TYPE_MINUS:
            parse_rule = self.prefix_parse_rules[token.type]
            exp = self.parse(parse_rule.precedence)
            return UnaryExpression('-', exp)
        elif token.type == TOKEN_TYPE_OPEN_PAREN:
            exp = self.parse()
            self.consume(TOKEN_TYPE_CLOSE_PAREN)
            return exp

    def parse_infix(self, left_expr, token):
        # token.type is gonna be exactly one of the keys in infix_parse_rules
        if token.type == TOKEN_TYPE_EXCLAMATION:
            return UnaryExpression('!', left_expr)
        else:
            parse_rule = self.infix_parse_rules[token.type]
            right_expr = self.parse(parse_rule.precedence - (1 if parse_rule.associativity == ASSOCIATIVITY_RIGHT else 0))
            return BinaryExpression(left_expr, token.value, right_expr)

    def peek(self):
        return self.tokens[self.pos]
    
    def consume(self, expected_token_type=None):
        token = self.peek()
        if expected_token_type and token.type != expected_token_type:
            raise Exception(f'Unexpected token {token}')
        if self.pos < len(self.tokens):
            self.pos += 1
        return token


### Usage
def parse_expr(expr_string):
    eval_val = Parser(tokenize(expr_string)).parse()
    print(f'"{expr_string}"  =>  "{eval_val}"')
    return eval_val

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        parse_expr(' '.join(sys.argv[1:]))
    else:
        assert str(parse_expr('3 * - ( - 1 + - 6 ! ) ^ 7 ^ 2 + 8 * 9')) == '(+ (* 3 (^ (- (+ (- 1) (- (! 6)))) (^ 7 2))) (* 8 9))'
        assert str(parse_expr('3 ^ - 5 !')) == '(^ 3 (- (! 5)))'
        assert str(parse_expr('1 / 3 / - 2 ! / 4 / 5')) == '(/ (/ (/ (/ 1 3) (- (! 2))) 4) 5)'
