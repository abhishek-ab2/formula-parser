import re
from typing import Iterable, Sized

from .types import Component, VALUE, VARIABLE

VARIABLE_REGEX = r'(\[\s*[a-zA-Z0-9_]+\s*\])'


def get_variables_in_formula(component: Component) -> set[VARIABLE]:
    variables = set()
    pattern = VARIABLE_REGEX
    matches = re.findall(pattern, component.formula)
    variables.update(matches)
    return variables


def _resolve_dependency(variable_name: VARIABLE, components: Iterable[Component]):
    comps: dict[VARIABLE, Component] = {c.name: c for c in components}
    deps: set[VARIABLE] = get_variables_in_formula(component=comps.get(variable_name, ''))
    to_process = deps.copy()
    while len(to_process):
        current = to_process.pop()
        deps.add(current)
        if current in to_process or current in deps:
            continue
        current_deps = _resolve_dependency(current, components)
        filtered_deps = list(filter(lambda x: x != current, current_deps))
        to_process.update(filtered_deps)
    return deps


def resolve_dependency_tree(components: Iterable[Component]):
    dependencies = {}
    for component in components:
        dependencies[component.name] = _resolve_dependency(component.name, components)
    return dependencies


def is_approx_equal(val1: VALUE, val2: VALUE, tolerance: float):
    return abs(abs(val1) - abs(val2)) <= tolerance


def value_len(item: Sized):
    return len(item)


def format_formula(formula: str):
    result = re.sub(VARIABLE_REGEX, lambda m: m.group(1)[1:-1].strip(), formula)
    return result.upper()


def round_off(value: float, precision: int = 2):
    return round(value, precision)
