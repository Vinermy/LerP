from dataclasses import dataclass
from enum import IntEnum, auto


class NodeType(IntEnum):
    PROGRAM = auto()
    NUMERIC_LITERAL = auto()
    IDENTIFIER = auto()
    BINARY_EXPRESSION = auto()
    NULL_LITETRAL = auto()


@dataclass
class Statement:
    kind: NodeType


@dataclass(repr=True)
class Program(Statement):
    body: list[Statement]
    kind = NodeType.PROGRAM


@dataclass
class Expression(Statement):
    pass

@dataclass
class BinaryExpression(Expression):
    left: Expression
    right: Expression
    operator: str
    kind = NodeType.BINARY_EXPRESSION


@dataclass
class Identifier(Expression):
    symbol: str
    kind = NodeType.IDENTIFIER

@dataclass
class NumericLiteral(Expression):
    value: float
    kind = NodeType.NUMERIC_LITERAL

@dataclass
class NullLiteral(Expression):
    value: str = "null"
    kind = NodeType.NULL_LITETRAL