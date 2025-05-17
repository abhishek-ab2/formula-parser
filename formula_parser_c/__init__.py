from .parser import Parser


def parse_formula(formulas: dict, initial_values: dict) -> dict:
    parser = Parser(formulas=formulas, values=initial_values)
    return parser.get_result()

