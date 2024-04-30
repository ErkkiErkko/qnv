import argparse
import sys
import numpy as np

from frontend.ast.tree import Program
from frontend.lexer import lexer
from frontend.parser import parser
from frontend.qnv.topology import Topology
from frontend.qnv.qnv import QNV
from utils.printtree import TreePrinter


def parseArgs():
    parser = argparse.ArgumentParser(description="Quantum Network Verifier")
    parser.add_argument("--input", type=str, help="the input qnv file")
    parser.add_argument("--parse", action="store_true", help="output parsed AST")
    parser.add_argument("--qnv", action="store_true", help="output semantic function result")
    parser.add_argument("--topo", type=str, help="the input topology file")
    return parser.parse_args()


def readCode(fileName):
    with open(fileName, "r") as f:
        return f.read()


# The parser stage: MiniDecaf code -> Abstract syntax tree
def step_parse(args: argparse.Namespace):
    code = readCode(args.input)
    r: Program = parser.parse(code, lexer=lexer)

    errors = parser.error_stack
    if errors:
        print("\n".join(map(str, errors)), file=sys.stderr)
        exit(1)

    return r


# The analysis stage: Abstract syntax tree -> Semantic function result
def step_qnv(args: argparse.Namespace, p: Program):
    f = open(args.topo, "r")
    topo = Topology(f)
    f.close()
    print("======Quantum Network Topology======")
    topo.print()
    print('')
    qnv = QNV(topo)
    res = qnv.analyse(p)
    return res


def main():
    args = parseArgs()

    def _parse():
        r = step_parse(args)
        return r

    def _qnv():
        tac = step_qnv(args, _parse())
        return tac

    if args.qnv:
        res = _qnv()
        print("======Quantum Network Verifier======")
        res.print()

    elif args.parse:
        prog = _parse()
        printer = TreePrinter(indentLen=2)
        printer.work(prog)

    return


if __name__ == "__main__":
    main()
