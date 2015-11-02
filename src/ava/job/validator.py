# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ast
import logging
from sys import version_info

from .errors import ScriptSyntaxError


supported_nodes = ('arg', 'assert', 'assign', 'attribute', 'augassign',
                   'binop', 'boolop', 'break', 'call', 'compare',
                   'continue', 'delete', 'dict', 'ellipsis',
                   'excepthandler', 'expr', 'extslice', 'for',
                   'if', 'ifexp', 'index', 'interrupt',
                   'list', 'listcomp', 'module', 'name', 'nameconstant',
                   'num', 'pass', 'raise', 'repr',
                   'slice', 'str', 'subscript', 'try', 'tuple', 'unaryop',)

reserved_names = (
    'eval', 'exec', 'print', '__getattribute'
)

_logger = logging.getLogger(__name__)


class ScriptValidator(ast.NodeVisitor):

    def __init__(self):
        self.node_handlers = dict(((node, getattr(self, "on_%s" % node))
                                   for node in supported_nodes))

    def validate(self, script, filename='<string>', mode='exec'):
        node = ast.parse(script, filename, mode)
        self.visit(node)

    def generic_visit(self, node):
        if node is None:
            return

        name = node.__class__.__name__.lower()
        # print("Node: %s" % name)
        if name not in supported_nodes:
            raise ScriptSyntaxError("Not supported node: %r" % name)

        try:
            handler = self.node_handlers[name]
            handler(node)
        except KeyError:
            raise ScriptSyntaxError("Not supported node: %r" % name)
        except SyntaxError as ex:
            raise ScriptSyntaxError(ex.message)

    def on_module(self, node):
        for tnode in node.body:
            self.visit(tnode)

    def on_expr(self, node):
        "expression"
        return self.visit(node.value)  # ('value',)

    def on_index(self, node):
        "index"
        return self.visit(node.value)  # ('value',)

    def on_return(self, node):  # ('value',)
        "return statement: look for None, return special sentinal"
        self.visit(node.value)

    def on_repr(self, node):
        "repr "
        self.visit(node.value)

    def on_pass(self, node):
        "pass statement"
        pass

    def on_ellipsis(self, node):
        "ellipses"
        pass

    # for break and continue: set the instance variable _interrupt
    def on_interrupt(self, node):    # ()
        "interrupt handler"
        pass

    def on_break(self, node):
        "break"
        pass

    def on_continue(self, node):
        "continue"
        pass

    def on_assert(self, node):    # ('test', 'msg')
        "assert statement"
        self.visit(node.test)

    def on_list(self, node):    # ('elt', 'ctx')
        "list"
        for e in node.elts:
            self.visit(e)

    def on_tuple(self, node):    # ('elts', 'ctx')
        "tuple"
        self.on_list(node)

    def on_dict(self, node):    # ('keys', 'values')
        "dictionary"
        for k, v in zip(node.keys, node.values):
            self.visit(k)
            self.visit(v)

    def on_num(self, node):   # ('n',)
        'return number'
        pass

    def on_str(self, node):   # ('s',)
        'return string'
        pass

    def on_name(self, node):    # ('id', 'ctx')
        """ Name node """
        name = node.id
        if name is None:
            return

        if name.startswith('__'):
            raise RuntimeError("Name with double underscores is not allowed: %s" % name)

        if name in reserved_names:
            raise RuntimeError("Reserved name: %s" % name)

    def on_nameconstant(self, node):
        """ True, False, None in python >= 3.4 """
        pass

    def on_attribute(self, node):    # ('value', 'attr', 'ctx')
        "extract attribute"
        pass

    def on_assign(self, node):    # ('targets', 'value')
        "simple assignment"
        self.visit(node.value)

    def on_augassign(self, node):    # ('target', 'op', 'value')
        "augmented assign"
        pass

    def on_slice(self, node):    # ():('lower', 'upper', 'step')
        "simple slice"
        self.visit(node.lower)
        self.visit(node.upper)
        self.visit(node.step)

    def on_extslice(self, node):    # ():('dims',)
        "extended slice"
        for tnode in node.dims:
            self.visit(tnode)

    def on_subscript(self, node):    # ('value', 'slice', 'ctx')
        "subscript handling -- one of the tricky parts"
        val = self.visit(node.value)
        nslice = self.visit(node.slice)

    def on_delete(self, node):    # ('targets',)
        "delete statement"
        pass

    def on_unaryop(self, node):    # ('op', 'operand')
        "unary operator"
        self.visit(node.operand)

    def on_binop(self, node):    # ('left', 'op', 'right')
        "binary operator"
        self.visit(node.left)
        self.visit(node.right)

    def on_boolop(self, node):    # ('op', 'values')
        "boolean operator"
        for n in node.values:
            self.visit(n)

    def on_compare(self, node):    # ('left', 'ops', 'comparators')
        "comparison operators"
        self.visit(node.left)
        for op, rnode in zip(node.ops, node.comparators):
            self.visit(rnode)

    def on_print(self, node):    # ('dest', 'values', 'nl')
        """ note: implements Python2 style print statement, not
        print() function.  May need improvement...."""
        self.visit(node.dest)
        for tnode in node.values:
            self.visit(tnode)

    def on_if(self, node):    # ('test', 'body', 'orelse')
        "regular if-then-else statement"
        self.visit(node.test)

        for tnode in node.orelse:
            self.visit(tnode)

        for tnode in node.body:
            self.visit(tnode)

    def on_ifexp(self, node):    # ('test', 'body', 'orelse')
        "if expressions"
        expr = node.orelse
        self.visit(node.test)
        self.visit(node.orelse)
        self.visit(node.body)

    def on_while(self, node):    # ('test', 'body', 'orelse')
        "while blocks"
        self.visit(node.test)
        for tnode in node.body:
            self.visit(tnode)

        for tnode in node.orelse:
            self.visit(tnode)

    def on_for(self, node):    # ('target', 'iter', 'body', 'orelse')
        "for blocks"

        for tnode in node.body:
            self.visit(tnode)

    def on_listcomp(self, node):    # ('elt', 'generators')
        "list comprehension"
        pass

    def on_excepthandler(self, node):  # ('type', 'name', 'body')
        "exception handler..."
        self.visit(node.type)

    def on_try(self, node):    # ('body', 'handlers', 'orelse', 'finalbody')
        "try/except/else/finally blocks"
        for tnode in node.body:
            self.visit(tnode)

    def on_raise(self, node):    # ('type', 'inst', 'tback')
        "raise statement: note difference for python 2 and 3"
        if version_info[0] == 3:
            excnode = node.exc
            msgnode = node.cause
        else:
            excnode = node.type
            msgnode = node.inst
        self.visit(excnode)
        self.visit(msgnode)

    def on_call(self, node):
        "function execution"
        #  ('func', 'args', 'keywords', 'starargs', 'kwargs')
        self.visit(node.func)

    def on_arg(self, node):    # ('test', 'msg')
        "arg for function definitions"
        pass

