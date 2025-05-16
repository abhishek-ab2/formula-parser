from pypackage import parse_formula
import pprint


val = {
    'CTC': 10000,
}

formulas = {
    'BASIC': 'IF([K], [CTC] * 0.5, [100])',
    'HRA': '[BASIC] + 100 + ([BASIC] + 100)',
    'HRA2': 'ROUND( MAX([HRA] + 100, 100000.51) )'
}

pprint.pprint(parse_formula(formulas, val, {
    'K': True
}))
