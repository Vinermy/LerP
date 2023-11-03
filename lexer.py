from dataclasses import dataclass
from enum import IntEnum, auto


class TokenType(IntEnum):
    # Literal types
    NULL = auto()
    NUMBER = auto()
    IDENTIFIER = auto()

    # Grouping and operators
    EQUALS = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    BINARY_OPERATOR = auto()
    EOF = auto()

    # Keywords
    VAR = auto()


KEYWORDS: dict[str, TokenType] = {
    "var": TokenType.VAR,
    "null": TokenType.NULL
}
@dataclass(repr=True)
class Token(object):
    value: str
    type: TokenType

def is_skippable(s: str) -> bool:
    return s in [' ', '\n', '\t']

def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    src = list(source)

    # Build each token until EoF
    while src:
        if src[0] == '(':
            tokens.append(Token(src.pop(0), TokenType.OPEN_PAREN))
        elif src[0] == ')':
            tokens.append(Token(src.pop(0), TokenType.CLOSE_PAREN))
        elif src[0] in ['+', '-', '*', '/', '%']:
            tokens.append(Token(src.pop(0), TokenType.BINARY_OPERATOR))
        elif src[0] == '=':
            tokens.append(Token(src.pop(0), TokenType.EQUALS))
        else:  # Handle multi-character tokens

            if src[0].isnumeric():
                num = ""
                while src and src[0].isnumeric():
                    num += src.pop(0)

                tokens.append(Token(num, TokenType.NUMBER))

            elif src[0].isalpha():
                ident = ""
                while src and src[0].isalpha():
                    ident += src.pop(0)

                # Check for reserved keywords
                try:
                    keyword = KEYWORDS[ident]
                except KeyError:
                    tokens.append(Token(ident, TokenType.IDENTIFIER))
                else:
                    tokens.append(Token(ident, keyword))

            elif is_skippable(src[0]):
                _ = src.pop(0)
            else:
                print(f"Unrecognized character found in source: {src[0]}")
                exit(7)

    tokens.append(Token("EndOfFile", TokenType.EOF))
    return tokens