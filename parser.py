import os
os.environ["PLY_YACC_DEBUG"] = "0"

from pyverilog.vparser.parser import parse
from pyverilog.vparser.ast import Identifier, IntConst, And, Or, Xor

def parse_verilog(file_path):
    ast, _ = parse(
        [file_path],
        preprocess_include=[],
        preprocess_define=[]
    )
    return ast


def expr_to_str(node):
    if isinstance(node, Identifier):
        return node.name
    elif isinstance(node, IntConst):
        return node.value
    elif isinstance(node, And):
        return f"({expr_to_str(node.left)} & {expr_to_str(node.right)})"
    elif isinstance(node, Or):
        return f"({expr_to_str(node.left)} | {expr_to_str(node.right)})"
    elif isinstance(node, Xor):
        return f"({expr_to_str(node.left)} ^ {expr_to_str(node.right)})"
    else:
        return str(node)


def extract_assignments(ast):
    assignments = []

    def visit(node):
        for c in node.children():
            if c.__class__.__name__ == "Assign":
                left = c.left.var.name

                right_node = c.right.var
                right = expr_to_str(right_node)

                signals = get_signals(right_node)

                assignments.append((left, right, signals))  # ✅ 3 values

            visit(c)

    visit(ast)
    return assignments

def get_signals(node):
    signals = []

    def visit(n):
        if n.__class__.__name__ == "Identifier":
            signals.append(n.name)
        for c in n.children():
            visit(c)

    visit(node)
    return signals