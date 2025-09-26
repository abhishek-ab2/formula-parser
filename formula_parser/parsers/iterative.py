from copy import deepcopy
from dataclasses import dataclass

from .base import BaseParser
from ..utils import is_approx_equal, round_off

TOLERANCE = 1
MAX_ITERATIONS = 100
MIN_ITERATIONS = 5


@dataclass
class Formula:
    formula: str
    variable: str
    is_fixed: bool


class IterativeParser(BaseParser):
    def __init__(self, max_iterations: int = MAX_ITERATIONS, min_iterations=MAX_ITERATIONS, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_iterations = max_iterations
        self.min_iterations = min_iterations
        self.total = list(self.values.values())[0]

    @staticmethod
    def _generate_formula_meta(formulas: dict[str, str]) -> dict[str, Formula]:
        res = {}
        for var, formula in formulas.items():
            try:
                float(formula)
                is_numeric = True
            except ValueError as e:
                print(e)
                is_numeric = False
            meta = Formula(
                    formula=formula,
                    variable=var,
                    is_fixed=is_numeric
            )
            res[var] = meta
        return res

    def parse(self, context: dict):
        iteration = 0
        current_total = 0
        context = context | self.values
        result = {}
        fixed_values = {}

        meta_formulas = self._generate_formula_meta(self.formulas)

        # Separate fixed values from formula ones
        for key, meta in meta_formulas.items():
            if meta.is_fixed:
                fixed_values[key] = float(meta.formula)
            else:
                result[key] = self.values.get(key, 0)

        # Evenly distribute values from
        init_value = round_off(self.total / len(result) * 2)
        for key, val in result.items():
            result[key] = init_value

        context |= fixed_values

        while (
                self.max_iterations > iteration and
                not is_approx_equal(current_total, self.total, TOLERANCE)
        ):
            prev_result = deepcopy(result)
            prev_total = current_total
            iteration += 1

            # Calculate the values of the variables
            for variable, formula in self.formulas.items():
                self._evaluate_formula(
                        variable=variable,
                        formula=formula,
                        result=result,
                        context=context
                )

            # Calculate the current total
            vals = list(result.values()) + list(fixed_values.values())
            current_total = sum(vals)

            # Find the difference between the current total and expected total
            scale = self.total / current_total

            for key in result:
                result[key] = round_off(result[key] * scale)

            if (abs(prev_total - self.total) < abs(current_total - self.total)) and iteration > self.min_iterations:
                return prev_result
        return result | fixed_values
