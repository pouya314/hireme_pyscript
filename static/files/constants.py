INITIAL_STATE = {
    "questions": (),
    "application_submitted": False
}

QUESTION_CATEGORY_ELIGIBILITY = "eligibility"
QUESTION_CATEGORY_APPLICATION = "application"
QUESTION_CATEGORIES = (
    QUESTION_CATEGORY_ELIGIBILITY, 
    QUESTION_CATEGORY_APPLICATION
)

# ######################################################

VALIDATIONS_REQUIRED = 'required'
VALIDATIONS_IS_STRING = 'is_string'
VALIDATIONS_IS_DECIMAL = 'is_decimal'

VALIDATIONS = (
    VALIDATIONS_REQUIRED,
    VALIDATIONS_IS_STRING,
    VALIDATIONS_IS_DECIMAL
)

# ######################################################

CONDITIONS_ANY = 'any'
CONDITIONS_EQUAL = 'equal'
CONDITIONS_GTE = 'gte'

CONDITIONS = (
    CONDITIONS_ANY,
    CONDITIONS_EQUAL,
    CONDITIONS_GTE
)
