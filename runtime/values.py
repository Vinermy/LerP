from dataclasses import dataclass
from enum import IntEnum, auto


class ValueType(IntEnum):
    NULL = auto()
    NUMBER = auto()

@dataclass
class RuntimeVal:
    type: ValueType


@dataclass
class NullVal(RuntimeVal):
    type: ValueType = ValueType.NULL
    value: str = "null"


@dataclass
class NumberVal(RuntimeVal):
    type: ValueType = ValueType.NUMBER
    value: float = .0
