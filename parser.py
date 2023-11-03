from lerp_ast import Statement, Program, Expression, BinaryExpression, NumericLiteral, Identifier, NodeType, NullLiteral
from lexer import tokenize, Token, TokenType


class Parser:
    tokens: list[Token] = []

    def not_eof(self) -> bool:
        if not self.tokens:
            return False
        return self.tokens[0].type != TokenType.EOF

    def at(self) -> Token:
        return self.tokens[0]

    def eat(self) -> Token:
        return self.tokens.pop(0)

    def produce_ast(self, sourceCode: str) -> Program:
        self.tokens = tokenize(sourceCode)
        program = Program(kind=NodeType.PROGRAM, body=[])

        while self.not_eof():
            program.body.append(self.parse_stmt())

        return program

    def parse_stmt(self) -> Statement:
        # Skip ro parse_expr
        return self.parse_expr()

    def parse_expr(self) -> Expression:
        return self.parse_additive_expr()

    # Orders of Prescidence:
    # ----------------------
    # - AssignmentExpr
    # - MemberExpr
    # - FunctionCall
    # - LogicalExpr
    # - ComparisonExpr
    # - AdditiveExpr
    # - MultiplicativeExpr
    # - UnaryExpr
    # - PrimaryExpr

    def parse_primary_expr(self) -> Expression:
        tk = self.at().type

        match tk:
            case TokenType.IDENTIFIER:
                return Identifier(kind=NodeType.IDENTIFIER, symbol=self.eat().value)
            case TokenType.NUMBER:
                return NumericLiteral(kind=NodeType.NUMERIC_LITERAL, value=float(self.eat().value))
            case TokenType.OPEN_PAREN:
                self.eat()  # Eat the opening paren
                value = self.parse_expr()
                self.expect(TokenType.CLOSE_PAREN, "No closing parenthesis was found")  # Eat the closing paren
                return value
            case TokenType.NULL:
                self.eat()  # Advance past NULL keyword
                return NullLiteral(NodeType.NULL_LITETRAL)

            case _:
                print("Unexpected token found during parsing: ", self.at().__repr__())
                exit(1)

    def parse_additive_expr(self) -> Expression:
        left = self.parse_multiplicative_expr()

        while self.at().value in ['+', '-']:
            operator = self.eat().value
            right = self.parse_multiplicative_expr()
            left = BinaryExpression(kind=NodeType.BINARY_EXPRESSION, left=left, right=right, operator=operator)

        return left

    def parse_multiplicative_expr(self) -> Expression:
        left = self.parse_primary_expr()

        while self.at().value in ['*', '/', '%']:
            operator = self.eat().value
            right = self.parse_primary_expr()
            left = BinaryExpression(kind=NodeType.BINARY_EXPRESSION, left=left, right=right, operator=operator)

        return left

    def expect(self, expect_type: TokenType, err):
        prev = self.tokens.pop(0)
        if not prev or prev.type != expect_type:
            print(f"Parser error: {err}, {prev} - expected {expect_type}")
            exit(1)