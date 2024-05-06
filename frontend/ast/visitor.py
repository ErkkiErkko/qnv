"""
Module that defines the base type of visitor.
"""


from __future__ import annotations

from typing import Callable, Protocol, Sequence, TypeVar

from .node import *
from .tree import *

T = TypeVar("T", covariant=True)
U = TypeVar("U", covariant=True)


def accept(visitor: Visitor[T, U], ctx: T) -> Callable[[Node], Optional[U]]:
    return lambda node: node.accept(visitor, ctx)


class Visitor(Protocol[T, U]):  # type: ignore
    def visitOther(self, node: Node, ctx: T) -> None:
        return None

    def visitNULL(self, that: NullType, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitProgram(self, that: Program, ctx: T) -> Optional[Sequence[Optional[U]]]:
        return self.visitOther(that, ctx)

    def visitIf(self, that: If, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitWhile(self, that: While, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitUnary(self, that: Unary, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    
    def visitBinary(self, that: Binary, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitAssignment(self, that: Assignment, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    
    def visitAssignmentCr(self, that: AssignmentCr, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    
    def visitAssignmentSw(self, that: AssignmentSw, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    
    def visitDe(self, that: De, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitAssertion(self, that: Assertion, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    
    def visitPass(self, that: Pass, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitIdentifierList(self, that: IdentifierList, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    
    def visitForget(self, that: Forget, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitIdentifier(self, that: Identifier, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)

    def visitIntLiteral(self, that: IntLiteral, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
