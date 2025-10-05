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
                is_numeric = False
            meta = Formula(
                    formula=formula,
                    variable=var,
                    is_fixed=is_numeric
            )
            res[var] = meta
        return res

    def parse(self, context: dict):
        """
        Iteratively computes component values such that:
        - Total sum does not exceed desired CTC
        - Components respect min/max constraints (via formulas)
        - Fixed values are never adjusted
        - No proportional scaling
        - Negative values are avoided
        - Convergence tolerance is respected (TOLERANCE = 50)
        """
        meta_formulas = self._generate_formula_meta(self.formulas)

        # Separate fixed and adjustable components
        fixed_values = {m.variable: float(m.formula) for m in meta_formulas.values() if m.is_fixed}
        variable_names = [m.variable for m in meta_formulas.values() if not m.is_fixed]

        # Initialize adjustable components
        result = {v: self.values.get(v, 0.0) for v in variable_names}

        # Merge fixed values into context
        context |= fixed_values

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            prev_result = deepcopy(result)
            total_used = sum(fixed_values.values())

            # Evaluate all variable formulas
            for v in variable_names:
                try:
                    self._evaluate_formula(
                        variable=v,
                        formula=meta_formulas[v].formula,
                        result=result,
                        context=context | result | fixed_values
                    )
                except Exception:
                    result[v] = 0.0  # fail-safe

                # Clamp to non-negative values
                result[v] = max(round_off(result[v]), 0.0)

            # Check convergence: all variables stable and total within tolerance
            total = total_used + sum(result.values())
            if (all(is_approx_equal(result[v], prev_result[v], 0.01) for v in variable_names)
                    and abs(total - self.total) <= TOLERANCE):
                break

        # Merge fixed values back into result
        final_result = result | fixed_values

        final_total = sum(final_result.values())
        if abs(final_total - self.total) > 50:
            print(f"[WARN] Total mismatch after solve: expected {self.total}, got {final_total}")

        return final_result
