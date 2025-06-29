from .parsers.iterative import IterativeParser
from .parsers.normal_parser import NormalParser
from .utils import format_formula, resolve_dependency_tree


def _format_formulas(formulas: dict):
    formatted = {}
    for var, formula in formulas.items():
        formatted[format_formula(var)] = format_formula(formula)
    return formatted


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


def parse(formulas, ini_values, context):
    dep_tree: dict = resolve_dependency_tree(formulas)
    formulas = _format_formulas(formulas)
    _format_dep_tree(dep_tree)

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
