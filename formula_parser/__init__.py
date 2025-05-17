
from .parser import parse
from .project_types import FORMULAS, VALUES, CONTEXT

__all__ = ['parse_formula']

def parse_formula(formulas: FORMULAS, initial_values: VALUES, context: CONTEXT) -> VALUES:
    return parse(formulas=formulas, ini_values=initial_values, context=context)

