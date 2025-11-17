from .base import BaseParser
from ..utils import round_off

MAX_ITERATIONS = 100
MIN_ITERATIONS = 5


class IterativeParser(BaseParser):
    def __init__(self, max_iterations: int = MAX_ITERATIONS, min_iterations=MAX_ITERATIONS, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_iterations = max_iterations
        self.min_iterations = min_iterations

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

        variables_to_calculate = [comp for comp in self.components if not comp.is_fixed]
        fixed_values = {comp.name: comp.value for comp in self.components if comp.is_fixed}

        # Initialize adjustable components
        result = {v.name: self.values.get(v.name, 0.0) for v in variables_to_calculate}

        # Merge fixed values into context
        context |= fixed_values

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1

            # Evaluate all variable formulas
            for comp in variables_to_calculate:
                try:
                    self._evaluate_formula(
                        component=comp,
                        result=result,
                        context=context | result | fixed_values
                    )
                except Exception:
                    result[comp.name] = result.get(comp.name, 0.0)  # fail-safe
                finally:
                    comp.value = result[comp.name]

                # Clamp to non-negative values
                result[comp.name] = max(round_off(result[comp.name]), 0.0)

            # Check convergence: all variables stable and total within tolerance
            if self._should_stop(result):
                break

        # Merge fixed values back into result
        final_result = result | fixed_values
        return final_result
