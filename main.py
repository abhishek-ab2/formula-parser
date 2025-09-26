from formula_parser import parse_formula
from formula_parser.parsers.exceptions import CustomException, get_error_desc

val = {'CTC': 12000}

formulas = {
"ADVANCE":"0",
"BASIC":"min(([CTC]-[EMPLOYER_PF]),if([EMPLOYEE_PF],if([CTC]<13000,[CTC]-[EMPLOYER_PF],max(13000,[CTC]*0.51)),"
        "if([CTC]<15100,[CTC],max(15100,[CTC]*0.51))))",
"BONUS":"min(([CTC]-[BASIC]-[EMPLOYER_PF]),[BASIC]*0.2)",
"EMPLOYER_ESIC":"if([EMPLOYEE_ESIC_APPLICABLE],[ESIC_WAGES]*3.25/100,0)",
"EMPLOYER_PF":"if([EMPLOYEE_PF],[PF_WAGES]*0.12,0)",
"EPF":"if([EMPLOYEE_PF],[PF_WAGES]*0.12,0)",
"ESIC":"if([EMPLOYEE_ESIC_APPLICABLE],[GROSS_SALARY]*0.75/100,0)",
"ESIC_WAGES":"if([EMPLOYEE_ESIC_APPLICABLE],[BASIC]+[HRA]+[BONUS]+[OTHER_ALLOWANCES]+[INCENTIVE],0)",
"GROSS_SALARY":"[BASIC]+[HRA]+[BONUS]+[OTHER_ALLOWANCES]+[INCENTIVE]",
"HRA":"min(([CTC]-[BASIC]-[EMPLOYER_PF]-[BONUS]),[BASIC]*0.3)",
"INCENTIVE":"0",
"NET_SALARY":"[GROSS_SALARY]-[TOTAL_DEDUCTION]",
"OTHER_1":"0",
"OTHER_ALLOWANCES":"[CTC]-[BASIC]-[HRA]-[BONUS]-[EMPLOYER_PF]",
"PF_WAGES":"if([EMPLOYEE_PF],min([BASIC]+[OTHER_ALLOWANCES],15000),[BASIC]+[OTHER_ALLOWANCES])",
"PT":"if([PT_WAGES]>12000,200,0)",
"PT_WAGES":"if([EMPLOYEE_PT_APPLICABLE],[BASIC]+[HRA]+[BONUS]+[OTHER_ALLOWANCES]+[INCENTIVE],0)",
"TDS":"0",
"TOTAL_DEDUCTION":"[EPF]+[ESIC]+[PT]+[TDS]+[ADVANCE]+[OTHER_1]",
}

try:
    res = parse_formula(
            formulas,
            val,
            {'EMPLOYEE_PF': True, 'EMPLOYEE_HIGHER_PF': False, 'EMPLOYEE_PF_PERCENT': 8, 'EMPLOYEE_WAGE_LIMIT_EMPLOYEE': False, 'EMPLOYEE_WAGE_LIMIT_COMPANY': False, 'EMPLOYEE_FPF_DEDUCTION': False, 'EMPLOYEE_ESIC_APPLICABLE': False, 'EMPLOYEE_PT_APPLICABLE': True}
    )
    print(res)
    print(f'Sum is {sum(list(res.values()))}')
except CustomException as e:
    print(e.message)
    print(e.description)
