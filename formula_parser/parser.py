from typing import Iterable

from .parsers.iterative import IterativeParser
from .parsers.normal_parser import NormalParser
from .types import Component
from .utils import format_formula, resolve_dependency_tree


def _initialize_comp_value(component: Component):
    try:
        component.value = float(component.formula)
        component.is_fixed = True
    except ValueError as e:
        component.is_fixed = False


def _format_formulas(components: Iterable[Component]):
    for comp in components:
        comp.formula = format_formula(comp.formula)
        _initialize_comp_value(comp)


def _format_dep_tree(dep_tree: dict[str, set[str]]):
    for var, deps in dep_tree.items():
        formatted = set()
        for dep in deps:
            formatted.add(format_formula(dep))
        dep_tree[var] = formatted


def _check_circular_dependency(dep_dict):
    def dfs(node, path):
        if node in path:
            return True
        path.add(node)
        for neighbor in dep_dict.get(node, []):
            if dfs(neighbor, path):
                return True
        path.remove(node)
        return False

    for var in dep_dict:
        if dfs(var, set()):
            return True
    return False


def _sort_components(components: Iterable[Component], dep_tree: dict[str, set[str]]):
    return sorted(components, key=lambda c: len(dep_tree.get(c.name) or []))


def parse(components: Iterable[Component], ini_values, context):
    _format_formulas(components)
    dep_tree: dict = resolve_dependency_tree(components)
    _format_dep_tree(dep_tree)

    components = _sort_components(components, dep_tree)
    if _check_circular_dependency(dep_tree):
        parser = IterativeParser(
            components=components,
            values=ini_values,
            dep_tree=dep_tree
        )
    else:
        parser = NormalParser(
            components=components,
            values=ini_values,
            dep_tree=dep_tree
        )

    return parser.get_result(context)
