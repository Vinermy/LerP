from pprint import pprint

from parser import Parser
from runtime.interpreter import evaluate

def LerP():
    parser = Parser()
    print("LerP v0.1 console interpreter")
    while True:
        s = input(">=> ")

        if not s or s == "exit":
            exit(1)

        program = parser.produce_ast(s)
        pprint(program.__repr__())
        result = evaluate(program)
        print(f"-> {result}")

if __name__ == "__main__":
    LerP()