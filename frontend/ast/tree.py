"""
Module that defines all AST nodes.
Reading this file to grasp the basic method of defining a new AST node is recommended.
Modify this file if you want to add a new AST node.
"""

from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar, Union

from utils import T, U

from .node import NULL, BinaryOp, Node, UnaryOp
from .visitor import Visitor, accept

_T = TypeVar("_T", bound=Node)
U = TypeVar("U", covariant=True)


def _index_len_err(i: int, node: Node):
    return IndexError(
        f"you are trying to index the #{i} child of node {node.name}, which has only {len(node)} children"
    )


class ListNode(Node, Generic[_T]):
    """
    Abstract node type that represents a node sequence.
    E.g. `Block` (sequence of statements).
    """

    def __init__(self, name: str, children: list[_T]) -> None:
        super().__init__(name)
        self.children = children

    def __getitem__(self, key: int) -> Node:
        return self.children.__getitem__(key)

    def __len__(self) -> int:
        return len(self.children)

    def accept(self, v: Visitor[T, U], ctx: T):
        ret = tuple(map(accept(v, ctx), self))
        return None if ret.count(None) == len(ret) else ret


class Program(ListNode["Statement"]):
    """
    AST root.
    """

    def __init__(self, *children: Statement) -> None:
        super().__init__("program", list(children))

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitProgram(self, ctx)


class Statement(Node):
    """
    Abstract type that represents a statement.
    """


class If(Statement):
    """
    AST node of if statement.
    """

    def __init__(
        self, cond: Expression, then: Program, otherwise: Program
    ) -> None:
        super().__init__("if")
        self.cond = cond
        self.then = then
        self.otherwise = otherwise

    def __getitem__(self, key: int) -> Node:
        return (self.cond, self.then, self.otherwise)[key]

    def __len__(self) -> int:
        return 3

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIf(self, ctx)


class While(Statement):
    """
    AST node of while statement.
    """

    def __init__(self, cond: Expression, body: Program) -> None:
        super().__init__("while")
        self.cond = cond
        self.body = body

    def __getitem__(self, key: int) -> Node:
        return (self.cond, self.body)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitWhile(self, ctx)


class Assignment(Statement):
    """
    AST node of assignment.
    """

    def __init__(
        self,
        ident: Identifier,
        expr: Expression,
    ) -> None:
        super().__init__("assignment")
        self.ident = ident
        self.expr = expr

    def __getitem__(self, key: int) -> Node:
        return (self.ident, self.expr)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitAssignment(self, ctx)
    

class AssignmentCr(Statement):
    """
    AST node of assignment (entanglement creation).
    """

    def __init__(
        self,
        ident: Identifier,
        expr1: Expression,
        expr2: Expression
    ) -> None:
        super().__init__("assignment_cr")
        self.ident = ident
        self.expr1 = expr1
        self.expr2 = expr2

    def __getitem__(self, key: int) -> Node:
        return (self.ident, self.expr1, self.expr2)[key]

    def __len__(self) -> int:
        return 3

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitAssignmentCr(self, ctx)
    

class AssignmentSw(Statement):
    """
    AST node of assignment (entanglement swapping).
    """

    def __init__(
        self,
        ident: Identifier,
        expr1: Expression,
        expr2: Expression,
        expr3: Expression
    ) -> None:
        super().__init__("assignment_sw")
        self.ident = ident
        self.expr1 = expr1
        self.expr2 = expr2
        self.expr3 = expr3

    def __getitem__(self, key: int) -> Node:
        return (self.ident, self.expr1, self.expr2, self.expr3)[key]

    def __len__(self) -> int:
        return 4

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitAssignmentSw(self, ctx)
    

class De(Statement):
    """
    AST node of de_statement.
    """

    def __init__(
        self,
        expr1: Expression,
        expr2: Expression
    ) -> None:
        super().__init__("de")
        self.expr1 = expr1
        self.expr2 = expr2

    def __getitem__(self, key: int) -> Node:
        return (self.expr1, self.expr2)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitDe(self, ctx)
    

class Assertion(Statement):
    """
    AST node of assertion.
    """

    def __init__(
        self,
        cond: Expression
    ) -> None:
        super().__init__("assertion")
        self.cond = cond

    def __getitem__(self, key: int) -> Node:
        return (self.cond)[key]

    def __len__(self) -> int:
        return 1

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitAssertion(self, ctx)


class Pass(Statement):
    """
    AST node of pass statement.
    """

    def __init__(
        self
    ) -> None:
        super().__init__("pass")

    def __getitem__(self, key: int) -> Node:
        return None

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitPass(self, ctx)
    

class IdentifierList(ListNode["Identifier"]):
    """
    AST node of identifier list.
    """

    def __init__(self, *children: Identifier) -> None:
        super().__init__("identifier_list", list(children))

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIdentifierList(self, ctx)

    def is_block(self) -> bool:
        return False
    

class Forget(Statement):
    """
    AST node of forget statement.
    """

    def __init__(
        self,
        ident_list: IdentifierList
    ) -> None:
        super().__init__("forget")
        self.ident_list = ident_list

    def __getitem__(self, key: int) -> Node:
        return (self.cond)[key]

    def __len__(self) -> int:
        return 1

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitForget(self, ctx)


class Expression(Node):
    """
    Abstract type that represents an evaluable expression.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.type: Optional[DecafType] = None


class Unary(Expression):
    """
    AST node of unary expression / test.
    Note that the operation type (like negative) is not among its children.
    """

    def __init__(self, op: UnaryOp, operand: Expression) -> None:
        super().__init__(f"unary({op.value})")
        self.op = op
        self.operand = operand

    def __getitem__(self, key: int) -> Node:
        return (self.operand,)[key]

    def __len__(self) -> int:
        return 1

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitUnary(self, ctx)

    def __str__(self) -> str:
        return "{}({})".format(
            self.op.value,
            self.operand,
        )


class Binary(Expression):
    """
    AST node of binary expression / test.
    Note that the operation type (like plus or subtract) is not among its children.
    """

    def __init__(self, op: BinaryOp, lhs: Expression, rhs: Expression) -> None:
        super().__init__(f"binary({op.value})")
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __getitem__(self, key: int) -> Node:
        return (self.lhs, self.rhs)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitBinary(self, ctx)

    def __str__(self) -> str:
        return "({}){}({})".format(
            self.lhs,
            self.op.value,
            self.rhs,
        )


class Identifier(Expression):
    """
    AST node of identifier "expression".
    """

    def __init__(self, value: str) -> None:
        super().__init__("identifier")
        self.value = value

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIdentifier(self, ctx)

    def __str__(self) -> str:
        return f"identifier({self.value})"

    def is_leaf(self):
        return True


class IntLiteral(Expression):
    """
    AST node of int literal like `0`.
    """

    def __init__(self, value: Union[int, str]) -> None:
        super().__init__("int_literal")
        self.value = int(value)

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIntLiteral(self, ctx)

    def __str__(self) -> str:
        return f"int({self.value})"

    def is_leaf(self):
        return True