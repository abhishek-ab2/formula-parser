from .utils import format_formula, resolve_dependency_tree, is_approx_equal, value_len
from .functions import CONTEXT

class BaseParser:
    def __init__(self, formulas: dict, values: dict):
        self.formulas = self._format_formulas(formulas)

        self.values = values
        self.dep_tree = None

    def parse(self, context: dict):
        raise NotImplementedError

    @staticmethod
    def _format_formulas(formulas: dict):
        formatted = {}
        for var, formula in formulas.items():
            formatted[format_formula(var)] = format_formula(formula)
        return formatted


    def get_result(self, context) -> dict:
        self.values = self.parse(self.values | context)
        return self.values
    
    def check_circular_dependency(self):
        self.dep_tree: dict = resolve_dependency_tree(self.formulas)
        circular_dep = False

        for variable, formula in self.dep_tree.items():
            circular_dep = circular_dep or variable in formula

        return circular_dep

    def evaluate_formula(self, variable: str, formula: str, result: dict, context: dict):
        if result.get(variable):
            return
        result[variable] = eval(formula, context, result)



class NormalParser(BaseParser):
    def parse(self, context):
        result = {}
        for key in self.formulas:
            result[key] = self.values.get(key, 0)
        res = {}



        for key in sorted(self.dep_tree, reverse=True, key=value_len):
            res[key] = result[key]

        for variable, formula in self.formulas.items():

            self.evaluate_formula(
                variable=variable,
                formula=formula,
                result=res,
                context=context
            )
            # print(f'{variable=} {formula=}')
            # print(res)
        return res
        
    

class IterativeParser(BaseParser):
    def __init__(self, formulas: dict, values: dict, max_iterations: int = 50, total: int=100):
        super().__init__(formulas=formulas, values=values)
        self.max_iterations = max_iterations
        self.total = total
    
    def parse(self, context: dict):
        iteration = 0
        actual_total = 0
        tolerance = 0.5
        precision = 2

        context = context | self.values

        result = {}

        for key in self.formulas:
            result[key] = self.values.get(key, 0)

        while (
            iteration < self.max_iterations and 
            not is_approx_equal(actual_total, self.total, tolerance)
            ):
            
            iteration += 1

            for variable, formula in self.formulas.items():
                self.evaluate_formula(
                    variable=variable,
                    formula=formula,
                    result=result,
                    context=context
                )
            
            vals = list(result.values())
            actual_total = round(sum(vals), 2)
        
        return result


class Parser(BaseParser):

    def get_result(self, context: CONTEXT) -> dict:
        if self.check_circular_dependency():
            parser = IterativeParser(formulas=self.formulas, values=self.values)
        else:
            parser = NormalParser(formulas=self.formulas, values=self.values)
        parser.dep_tree = self.dep_tree
        parser.formulas = self.formulas
        return parser.get_result(CONTEXT | context)
