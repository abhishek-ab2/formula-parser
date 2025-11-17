from typing import Iterable

from .parser import parse
from .types import Component, CONTEXT, FORMULAS, VALUES

__all__ = ['parse_formula']


def parse_formula(components: Iterable[Component], initial_values: VALUES, context: CONTEXT) -> VALUES:
    return parse(components=components, ini_values=initial_values, context=context)
