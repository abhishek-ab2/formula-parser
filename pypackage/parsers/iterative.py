from .base import BaseParser
from ..utils import is_approx_equal

class IterativeParser(BaseParser):
    def __init__(self, max_iterations: int = 50, total: int = 100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_iterations = max_iterations
        self.total = total

    def parse(self, context: dict):
        iteration = 0
        actual_total = 0
        tolerance = 1

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
                self._evaluate_formula(
                        variable=variable,
                        formula=formula,
                        result=result,
                        context=context
                )

            vals = list(result.values())
            actual_total = round(sum(vals), 2)

        return result