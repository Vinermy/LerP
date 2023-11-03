from .values import ValueType, RuntimeVal, NumberVal, NullVal
from lerp_ast import NodeType, Statement, NumericLiteral, BinaryExpression, Program


def evaluate_program(program: Program) -> RuntimeVal:
    last_evaluated: RuntimeVal = NullVal()

    for statement in program.body:
        last_evaluated = evaluate(statement)

    return last_evaluated


def evaluate_numeric_expression(left_hand_side: NumberVal, right_hand_side: NumberVal, operator: str) -> NumberVal:
    result = 0
    match operator:
        case '+':
            result = left_hand_side.value + right_hand_side.value
        case '-':
            result = left_hand_side.value - right_hand_side.value
        case '*':
            result = left_hand_side.value * right_hand_side.value
        case '/':
            # TODO: Division by zero check
            result = left_hand_side.value / right_hand_side.value
        case '%':
            result = left_hand_side.value % right_hand_side.value

    return NumberVal(value=result)


def evaluate_binary_expression(binop: BinaryExpression) -> RuntimeVal:
    left_hand_side: RuntimeVal = evaluate(binop.left)
    right_hand_side: RuntimeVal = evaluate(binop.right)

    if left_hand_side.type == ValueType.NUMBER and right_hand_side.type == ValueType.NUMBER:
        left_hand_side: NumberVal
        right_hand_side: NumberVal
        return evaluate_numeric_expression(left_hand_side, right_hand_side, binop.operator)

    return NullVal()


def evaluate(astNode: Statement) -> RuntimeVal:
    match astNode.kind:
        case NodeType.NUMERIC_LITERAL:
            astNode: NumericLiteral
            return NumberVal(value=astNode.value)

        case NodeType.BINARY_EXPRESSION:
            astNode: BinaryExpression
            return evaluate_binary_expression(binop=astNode)

        case NodeType.PROGRAM:
            astNode: Program
            return evaluate_program(program=astNode)

        case NodeType.NULL_LITETRAL:
            return NullVal()
        case _:
            print("This AST node has not yet been setup for interpretation", astNode)
            exit(1)
