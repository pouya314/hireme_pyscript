from typing import List, Dict

from toolz import assoc_in

from .helpers import get_data


def initialize_action(state, action):
    print("performing `initialize_action()` on state: {}".format(state))

    # Read and sort the data
    sorted_eligibility_questions: List[Dict] = sorted(get_data("questions.json"), key=lambda question: question['position'])
    sorted_application_questions: List[Dict] = sorted(get_data("application.json"), key=lambda question: question['position'])

    # Prepare the state for initial load
    state_with_sorted_eligibility_qs = assoc_in(state, ["eligibility_questions"], sorted_eligibility_questions)
    state_with_sorted_application_qs = assoc_in(state_with_sorted_eligibility_qs, ["application_questions"], sorted_application_questions)
    state_with_current_q = assoc_in(state_with_sorted_application_qs, ["current_question"], sorted_eligibility_questions[0])

    return state_with_current_q


def submit_action(state, action):
    print("performing `submit_action()` on state: {}".format(state))
    return state
