from .base import BaseParser
from ..utils import value_len


class NormalParser(BaseParser):
    def parse(self, context):
        result = {}
        for key in self.formulas:
            result[key] = self.values.get(key, 0)

        res = {}
        for key in sorted(self.dep_tree, reverse=True, key=value_len):
            res[key] = result[key]

        for variable, formula in self.formulas.items():
            self._evaluate_formula(
                    variable=variable,
                    formula=formula,
                    result=res,
                    context=context
            )

        return res
