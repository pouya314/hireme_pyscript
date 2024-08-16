from typing import List, Dict

from toolz import get_in, assoc_in

from .helpers import get_data


def initialize_action(state, action):
    print("performing `initialize_action()` on state: {}".format(state))
    eligibility_questions: List[Dict] = get_data('questions.json')
    application_questions: List[Dict] = get_data('application.json')
    # sorted(eligibility_questions, key=lambda question: question['position'])
    state_with_eligibility_qs = assoc_in(state, ['eligibility_questions'], eligibility_questions)
    return assoc_in(state_with_eligibility_qs, ['application_questions'], application_questions)


def submit_action(state, action):
    print("performing `submit_action()` on state: {}".format(state))
    return state
