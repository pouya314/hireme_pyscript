from . import mappings
from . import errors


def validate(question):
    """
    Validate the provided answer against the question's validations.
    """
    validation_errors = []
    for validation in question['validations']:
        try:
            mappings.Validations[validation](question["provided_answer"])
        except errors.ValidationError as e:
            validation_errors.append(str(e))

    return (False, validation_errors) if validation_errors else (True, ())
