import re
from .project_types import *
from typing import Sized

VARIABLE_REGEX = r'(\[\s*[a-zA-Z0-9_]+\s*\])'
FORMATTED_VAR_REGEX = r'\[([a-zA-Z0-9_]+)\]'


def get_variables_in_formula(formula: FORMULA) -> set[VARIABLE]:
    variables = set()
    pattern = FORMATTED_VAR_REGEX
    matches = re.findall(pattern, formula)
    variables.update(matches)
    return variables

def _resolve_dependency(variable_name: VARIABLE, formulas: FORMULAS):
    deps: set[VARIABLE] = get_variables_in_formula(formula=formulas.get(variable_name, ''))
    to_process = deps.copy()
    while len(to_process):
        current = to_process.pop()
        deps.add(current)
        if current in to_process or current in deps:
            continue
        current_deps = _resolve_dependency(current, formulas)
        filtered_deps = list(filter(lambda x: x != current, current_deps))
        to_process.update(filtered_deps)
    return deps

def resolve_dependency_tree(formulas: FORMULAS):
    dependencies = {}
    for variable in formulas:
        dependencies[variable] = _resolve_dependency(variable, formulas)
    return dependencies


def is_approx_equal(val1: VALUE, val2: VALUE, tolerance: float):
    return (abs(val1) - abs(val2)) <= tolerance

def value_len(item: Sized):
    return len(item)


def format_formula(formula: str):
    result = re.sub(VARIABLE_REGEX, lambda m: m.group(1)[1:-1].strip(), formula)
    return result

