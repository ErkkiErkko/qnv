import numpy as np

from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from frontend.ast import node
from frontend.qnv.topology import Topology
from frontend.qnv.configuration import *
from utils.error import *

class QNV(Visitor[PConfiguration, list]):
    def __init__(self, topo: Topology):
        self.topo = topo

    def analyse(self, program: Program):
        ctx = PConfiguration([DConfiguration({}, np.zeros((self.topo.n, self.topo.n), dtype=int))])
        program.accept(self, ctx)
        return ctx
    
    def visitProgram(self, program: Program, ctx: PConfiguration) -> None:
        for stmt in program.children:
            stmt.accept(self, ctx)

    def visitIf(self, stmt: If, ctx: PConfiguration) -> None:
        retc = stmt.cond.accept(self, ctx)
        ctx1 = PConfiguration(list())
        ctx0 = PConfiguration(list())
        for i in range(0, len(ctx.dconfs)):
            if retc[i] != 0:
                ctx1.dconfs.append(ctx.dconfs[i])
            else:
                ctx0.dconfs.append(ctx.dconfs[i])
        stmt.then.accept(self, ctx1)
        stmt.otherwise.accept(self, ctx0)
        ctx.dconfs = ctx1.dconfs + ctx0.dconfs

    def visitWhile(self, stmt: While, ctx: PConfiguration) -> None:
        ctx0_dconfs = list()
        loop_cnt = 0
        while True:
            retc = stmt.cond.accept(self, ctx)
            ctx1_dconfs = list()
            for i in range(0, len(ctx.dconfs)):
                if retc[i] != 0:
                    ctx1_dconfs.append(ctx.dconfs[i])
                else:
                    ctx0_dconfs.append(ctx.dconfs[i])
            if len(ctx1_dconfs) == 0:
                break
            ctx.dconfs = ctx1_dconfs
            stmt.body.accept(self, ctx)
            loop_cnt = loop_cnt + 1
            if loop_cnt > 1000:
                print("Error: Too many loops.")
                exit()
        ctx.dconfs = ctx0_dconfs

    def visitAssignment(self, stmt: Assignment, ctx: PConfiguration) -> None:
        rete = stmt.expr.accept(self, ctx)
        ctx.assign(stmt.ident.value, rete)

    def visitAssignmentCr(self, stmt: AssignmentCr, ctx: PConfiguration) -> None:
        ret1 = stmt.expr1.accept(self, ctx)
        ret2 = stmt.expr2.accept(self, ctx)
        ctx.cr(stmt.ident.value, ret1, ret2, self.topo)

    def visitAssignmentSw(self, stmt: AssignmentSw, ctx: PConfiguration) -> None:
        ret1 = stmt.expr1.accept(self, ctx)
        ret2 = stmt.expr2.accept(self, ctx)
        ret3 = stmt.expr3.accept(self, ctx)
        ctx.sw(stmt.ident.value, ret1, ret2, ret3, self.topo)
    
    def visitAssertion(self, stmt: Assertion, ctx: PConfiguration) -> None:
        retc = stmt.cond.accept(self, ctx)
        ctx1 = PConfiguration(list())
        for i in range(0, len(ctx.dconfs)):
            if retc[i] != 0:
                ctx1.dconfs.append(ctx.dconfs[i])
        ctx.dconfs = ctx1.dconfs
    
    def visitIdentifierList(self, node: IdentifierList, ctx: PConfiguration) -> None:
        pass
    
    def visitForget(self, stmt: Forget, ctx: PConfiguration) -> None:
        stmt.ident_list.accept(self, ctx)
        new_ctx = PConfiguration(list())
        for dconf in ctx.dconfs:
            for ident in stmt.ident_list.children:
                dconf.mem.pop(ident.value)
            in_new_ctx = False
            for new_dconf in new_ctx.dconfs:
                if dconf.mem == new_dconf.mem and dconf.ent == new_dconf.ent:
                    in_new_ctx = True
                    new_dconf.prob = new_dconf.prob + dconf.prob
                    break
            if not in_new_ctx:
                new_ctx.dconfs.append(dconf)
        ctx.dconfs = new_ctx.dconfs
                
    def visitUnary(self, expr: Unary, ctx: PConfiguration) -> list:
        reto = expr.operand.accept(self, ctx)
        ret = list()
        for i in range(0, len(reto)):
            ret.append({
                node.UnaryOp.Neg: -reto[i],
                node.UnaryOp.LogicNot: int(not reto[i])
            }[expr.op])
        return ret
    
    def visitBinary(self, expr: Binary, ctx: PConfiguration) -> list:
        retl = expr.lhs.accept(self, ctx)
        retr = expr.rhs.accept(self, ctx)
        ret = list()
        for i in range(0, len(retl)):
            ret.append({
                node.BinaryOp.Add: retl[i] + retr[i],
                node.BinaryOp.Sub: retl[i] - retr[i],
                node.BinaryOp.Mul: retl[i] * retr[i],
                node.BinaryOp.Div: (retl[i] // retr[i]) if retr[i] != 0 else None,
                node.BinaryOp.LogicOr: int(retl[i] or retr[i]),
                node.BinaryOp.LogicAnd: int(retl[i] and retr[i]),
                node.BinaryOp.EQ: int(retl[i] == retr[i]),
                node.BinaryOp.NE: int(retl[i] != retr[i]),
                node.BinaryOp.LT: int(retl[i] < retr[i]),
                node.BinaryOp.LE: int(retl[i] <= retr[i]),
                node.BinaryOp.GT: int(retl[i] > retr[i]),
                node.BinaryOp.GE: int(retl[i] >= retr[i])
            }[expr.op])
        return ret
    
    def visitIdentifier(self, ident: Identifier, ctx: PConfiguration) -> list:
        ret = list()
        for dconf in ctx.dconfs:
            ret.append(dconf.mem[ident.value])
        return ret

    def visitIntLiteral(self, expr: IntLiteral, ctx: PConfiguration) -> list:
        ret = list()
        for i in range(0, len(ctx.dconfs)):
            ret.append(expr.value)
        return ret