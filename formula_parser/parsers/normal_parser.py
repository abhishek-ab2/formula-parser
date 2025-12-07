from .base import BaseParser


class NormalParser(BaseParser):
    def parse(self, context):
        result = {**self.values}

        variables_to_calculate = [comp for comp in self.components if not comp.is_fixed]
        fixed_variables = [comp for comp in self.components if comp.is_fixed]

        # for comp in self.components:
        #     result[comp.name] = self.values.get(comp.name, 0)

        context |= {comp.name: comp.value for comp in fixed_variables}

        for variable in variables_to_calculate:
            self._evaluate_formula(
                component=variable,
                result=result,
                context=context | result
            )

        return result
