from formula_parser.functions import FUNCTIONS
from .exceptions import CustomException, get_custom_error, get_error_desc


class BaseParser:
    def __init__(self, formulas: dict, values: dict, dep_tree: dict):
        self.formulas = formulas

        self.values = values
        self.dep_tree = dep_tree

    def parse(self, context: dict):
        raise NotImplementedError

    def get_result(self, context) -> dict:
        self.values = self.parse(self.values | FUNCTIONS | context)
        return self.values

    @staticmethod
    def _evaluate_formula(variable: str, formula: str, result: dict, context: dict):
        try:
            result[variable] = eval(formula, context, result)
        except Exception as e:
            error: type[CustomException] = get_custom_error(e)
            print(f'''
                {variable=}
                {str(e)=}
                {get_error_desc(e)=}
''')
            raise error(field=variable, message=str(e), description=get_error_desc(e))
