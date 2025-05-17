from formula_parser import parse_formula


val = {
    'CTC': 10000,
}

formulas = {
    'BASIC': 'IF( [EMPLOYEE_PF], [CTC] * 0.5, 100)',
    'HRA': '[BASIC] + 100 + ([BASIC] + 100)',
    'HRA2': 'ROUND( MAX([HRA] + 100, 100000.51) )'
}

res = parse_formula(
        formulas,
        val,
        {
            'EMPLOYEE_PF': True
        }
)
