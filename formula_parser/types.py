import dataclasses
from enum import Enum

class ComponentType(Enum):
    ALLOWANCE = 0
    DEDUCTION = 1

@dataclasses.dataclass
class Component:
    name: str
    formula: str
    is_fixed: bool
    type: ComponentType


