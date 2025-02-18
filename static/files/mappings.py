from . import constants
from . import validations
from . import conditions


Validations = {
    constants.VALIDATIONS_REQUIRED: validations.required,
    constants.VALIDATIONS_IS_STRING: validations.is_string,
    constants.VALIDATIONS_IS_DECIMAL: validations.is_decimal
}

Conditions = {
    constants.CONDITIONS_ANY: conditions.any,
    constants.CONDITIONS_EQUAL: conditions.equal,
    constants.CONDITIONS_GTE: conditions.gte
}
