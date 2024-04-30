"""
Module that defines a parser using `ply.yacc`.
Add your own parser rules on demand, which can be accomplished by:

1. Define a global function whose name starts with "p_".
2. Write the corresponding grammar rule(s) in its docstring.
3. Complete the function body, which is actually a syntax base translation process.
    We're using this technique to build up the AST.

Refer to https://www.dabeaz.com/ply/ply.html for more details.
"""


import ply.yacc as yacc

from frontend.ast.tree import *
from frontend.lexer import lex
from utils.error import DecafSyntaxError

tokens = lex.tokens
error_stack = list[DecafSyntaxError]()


def unary(p):
    p[0] = Unary(UnaryOp.backward_search(p[1]), p[2])


def binary(p):
    if p[2] == BinaryOp.Assign.value:
        p[0] = Assignment(p[1], p[3])
    else:
        p[0] = Binary(BinaryOp.backward_search(p[2]), p[1], p[3])


def p_empty(p: yacc.YaccProduction):
    """
    empty :
    """
    pass


def p_program(p):
    """
    program : program statement
    """
    if p[2] is not NULL:
        p[1].children.append(p[2])
    p[0] = p[1]


def p_program_empty(p):
    """
    program : empty
    """
    p[0] = Program()


def p_statement(p):
    """
    statement : assignment
        | assignment_cr
        | assignment_sw
        | assertion
        | pass_statement
        | forget_statement
    """
    p[0] = p[1]


def p_if_else(p):
    """
    statement : If LParen test RParen LBrace program RBrace Else LBrace program RBrace
    """
    p[0] = If(p[3], p[6], p[10])


def p_while(p):
    """
    statement : While LParen test RParen LBrace program RBrace
    """
    p[0] = While(p[3], p[6])


def p_assignment(p):
    """
    assignment : Identifier Assign expression Semi
    """
    p[0] = Assignment(p[1], p[3])


def p_assignment_cr(p):
    """
    assignment_cr : Identifier Assign Cr LParen expression Comma expression RParen Semi
    """
    p[0] = AssignmentCr(p[1], p[5], p[7])


def p_assignment_sw(p):
    """
    assignment_sw : Identifier Assign Sw LParen expression Comma expression At expression RParen Semi
    """
    p[0] = AssignmentSw(p[1], p[5], p[7], p[9])


def p_assertion(p):
    """
    assertion : Assert LParen test RParen Semi
    """
    p[0] = Assertion(p[3])


def p_pass(p):
    """
    pass_statement : Pass Semi
    """
    p[0] = Pass()


def p_identifier_list(p):
    """
    IdentifierList : Identifier IdentifierListCommaAhead
    """
    if p[1] is not NULL:
        p[2].children = [p[1]] + p[2].children
    p[0] = p[2]


def p_identifier_list_comma_ahead(p):
    """
    IdentifierListCommaAhead : Comma Identifier IdentifierListCommaAhead
    """
    if p[2] is not NULL:
        p[3].children = [p[2]] + p[3].children
    p[0] = p[3]


def p_identifier_list_empty(p):
    """
    IdentifierList : empty
    """
    p[0] = IdentifierList()


def p_identifier_list_comma_ahead_empty(p):
    """
    IdentifierListCommaAhead : empty
    """
    p[0] = IdentifierList()


def p_forget(p):
    """
    forget_statement : Forget LParen IdentifierList RParen Semi
    """
    p[0] = Forget(p[3])


def p_expression_precedence(p):
    """
    expression : additive
    additive : multiplicative
    multiplicative : unary
    unary : postfix
    postfix : primary
    """
    p[0] = p[1]


def p_unary_expression(p):
    """
    unary : Minus unary
    """
    unary(p)


def p_binary_expression(p):
    """
    additive : additive Plus multiplicative
        | additive Minus multiplicative
    multiplicative : multiplicative Mul unary
        | multiplicative Div unary
    """
    binary(p)


def p_int_literal_expression(p):
    """
    primary : Integer
    """
    p[0] = p[1]


def p_identifier_expression(p):
    """
    primary : Identifier
    """
    p[0] = p[1]


def p_brace_expression(p):
    """
    primary : LParen expression RParen
    """
    p[0] = p[2]


def p_test_precedence(p):
    """
    test : logical_or
    logical_or : logical_and
    logical_and : relational
    """
    p[0] = p[1]


def p_unary_test(p):
    """
    relational : Not relational
    """
    unary(p)


def p_binary_test(p):
    """
    logical_or : logical_or Or logical_and
    logical_and : logical_and And relational
    relational : expression NotEqual expression
        | expression Equal expression
        | expression Less expression
        | expression Greater expression
        | expression LessEqual expression
        | expression GreaterEqual expression
    """
    binary(p)


def p_error(t):
    """
    A naive (and possibly erroneous) implementation of error recovering.
    """
    if not t:
        error_stack.append(DecafSyntaxError(t, "EOF"))
        return

    inp = t.lexer.lexdata
    error_stack.append(DecafSyntaxError(t, f"\n{inp.splitlines()[t.lineno - 1]}"))

    parser.errok()
    return parser.token()


parser = yacc.yacc(start="program")
parser.error_stack = error_stack  # type: ignore
