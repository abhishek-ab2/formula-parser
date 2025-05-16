from pypackage.functions import FUNCTIONS


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
        if result.get(variable):
            return
        result[variable] = eval(formula, context, result)