from . import mappings


def validate(question):
    return mappings.Conditions[question['condition']](question)
