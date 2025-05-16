import pprint

from .parser import Parser
from .project_types import FORMULAS, VALUES, CONTEXT

def parse_formula(formulas: FORMULAS, initial_values: VALUES, context: CONTEXT) -> VALUES:
    ps = Parser(formulas=formulas, values=initial_values)
    return ps.get_result(context)

