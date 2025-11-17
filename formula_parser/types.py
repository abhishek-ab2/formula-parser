from dataclasses import dataclass
from enum import Enum


class SalaryStructures(Enum):
    CTC = 'CTC'
    GROSS = 'GROSS'


class ComponentType(Enum):
    ALLOWANCE = 0
    DEDUCTION = 1
    EMPLOYER_ALLOWANCE = 2


@dataclass
class Component:
    name: str
    formula: str
    is_fixed: bool
    type: ComponentType
    value: float


FORMULA = str
VARIABLE = str
VALUE = int | float
CONTEXT = dict[FORMULA, VALUE]
FORMULAS = dict[VARIABLE, FORMULA]
VALUES = dict[VARIABLE, VALUE | bool]
