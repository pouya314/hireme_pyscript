from . import mappings


def perform(question):
    return mappings.Conditions[question['condition']](question)
