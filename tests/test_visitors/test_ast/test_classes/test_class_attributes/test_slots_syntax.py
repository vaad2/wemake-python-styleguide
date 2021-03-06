# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    IncorrectSlotsViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongSlotsVisitor

class_body_template = """
class ClassWithSlots(object):
    __slots__ = {0}
"""


@pytest.mark.parametrize('code', [
    '[]',
    '("a", "a")',
    '(1,)',
    '(variable,)',
    '{"name"}',
    '{1, 2}',
])
def test_incorrect_slots(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that incorrect slots are prohibited."""
    tree = parse_ast_tree(class_body_template.format(code))

    visitor = WrongSlotsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [IncorrectSlotsViolation])


@pytest.mark.parametrize('code', [
    '()',
    '("a",)',
    '("a", "b")',
    'SomeOther.__slots__',
    'SomeOther.__slots__ + ("child",)',
    'SomeOther.__slots__ + {"child"}',
    'some_call()',
])
def test_correct_slots(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that correct slots are allowed."""
    tree = parse_ast_tree(class_body_template.format(code))

    visitor = WrongSlotsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
