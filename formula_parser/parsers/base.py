from typing import Iterable

from formula_parser.functions import FUNCTIONS
from .exceptions import CustomException, get_custom_error, get_error_desc
from ..types import Component, ComponentType, SalaryStructures
from ..utils import is_approx_equal, round_off


class BaseParser:
    TOLERANCE = 1

    def __init__(self, components: Iterable[Component], values: dict, dep_tree: dict[str, set]):
        self.values = values
        self.dep_tree = dep_tree
        assert len(self.values) >= 1
        self.components = sorted(components, key=lambda c: len(self.dep_tree[c.name]), reverse=True)
        self.structure = SalaryStructures(list(self.values.keys())[0])
        self.total = list(self.values.values())[0]

    def parse(self, context: dict):
        raise NotImplementedError

    def get_result(self, context) -> dict:
        self.values = self.parse(self.values | FUNCTIONS | context)
        return self.values

    @staticmethod
    def _evaluate_formula(component: Component, result: dict, context: dict):
        try:
            result[component.name] = max(round_off(eval(component.formula, context, result)), 0)
        except Exception as e:
            error: type[CustomException] = get_custom_error(e)
            print(
                f'''
                {component.name=}
                {str(e)=}
                {get_error_desc(e)=}
'''
            )

            raise error(field=component.name, message=str(e), description=get_error_desc(e))

    def _should_stop(self, result: dict) -> bool:
        ctc = sum(result.get(comp.name, 0.0) for comp in self.components if comp.type == ComponentType.ALLOWANCE)
        total = ctc
        if self.structure == SalaryStructures.CTC:
            deductions = sum(
                result.get(comp.name, 0) for comp in self.components if comp.type == ComponentType.DEDUCTION
            )
            total = total - deductions

        return is_approx_equal(self.total, total, self.TOLERANCE)
