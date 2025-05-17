from .parsers.base import BaseParser
from .parsers.iterative import IterativeParser
from .parsers.normal_parser import NormalParser
from .utils import format_formula, resolve_dependency_tree


def _format_formulas(formulas: dict):
    formatted = {}
    for var, formula in formulas.items():
        formatted[format_formula(var)] = format_formula(formula)
    return formatted


def _check_circular_dependency(dep_tree):
    circular_dep = False

    for variable, formula in dep_tree.items():
        circular_dep = circular_dep or (variable in formula)

    return circular_dep


def parse(formulas, ini_values, context):
    formulas = _format_formulas(formulas)
    dep_tree: dict = resolve_dependency_tree(formulas)
    if _check_circular_dependency(dep_tree):
        parser = IterativeParser(
                formulas=formulas,
                values=ini_values,
                dep_tree=dep_tree
        )
    else:
        parser = NormalParser(
                formulas=formulas,
                values=ini_values,
                dep_tree=dep_tree
        )

    return parser.get_result(context)
