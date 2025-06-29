from copy import deepcopy

from .base import BaseParser
from ..utils import is_approx_equal

TOLERANCE = 1

class IterativeParser(BaseParser):
    def __init__(self, max_iterations: int = 50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_iterations = max_iterations
        self.total = list(self.values.values())[0]

    def parse(self, context: dict):
        iteration = 0
        current_total = 0
        context = context | self.values
        result = {}

        for key in self.formulas:
            result[key] = self.values.get(key, 0)

        while (
            iteration < self.max_iterations and
            not is_approx_equal(current_total, self.total, TOLERANCE)
        ):
            prev_result = deepcopy(result)
            prev_total = current_total
            iteration += 1

            for variable, formula in self.formulas.items():
                self._evaluate_formula(
                        variable=variable,
                        formula=formula,
                        result=result,
                        context=context
                )

            vals = list(result.values())
            current_total = round(sum(vals), 2)

            if abs(prev_total - self.total) < abs(current_total - self.total):
                return prev_result

        return result