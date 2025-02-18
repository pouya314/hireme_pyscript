from decimal import Decimal


def any(question):
    accepted = True
    error = None

    if question['provided_answer'] not in question['accepted_answers']:
        accepted = False
        error = question['message_if_fail']

    return accepted, error


def equal(question):
    accepted = True
    error = None

    if question['provided_answer'] != question['accepted_answers'][0]:
        accepted = False
        error = question['message_if_fail']

    return accepted, error


def gte(question):
    accepted = True
    error = None

    if Decimal(question['provided_answer']) < Decimal(question['accepted_answers'][0]):
        accepted = False
        error = question['message_if_fail']

    return accepted, error
