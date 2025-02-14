from typing import List, Dict

from toolz import assoc_in, concat

from .helpers import get_data
from .constants import QUESTION_CATEGORY_ELIGIBILITY, QUESTION_CATEGORY_APPLICATION


def initialize_action(state, action):
    print("performing `initialize_action()` on state: {}".format(state))

    eligibility_questions: List[Dict] = [
        assoc_in(question, ["category"], QUESTION_CATEGORY_ELIGIBILITY) 
        for question in get_data("questions.json")
    ]
    application_questions: List[Dict] = [
        assoc_in(question, ["category"], QUESTION_CATEGORY_APPLICATION) 
        for question in get_data("application.json")
    ]

    all_questions = tuple(concat([eligibility_questions, application_questions]))

    for question in all_questions:
        question["provided_answer"] = None
        question["validation_errors"] = []
        question["acceptance_errors"] = []

    state_with_questions_populated = assoc_in(state, ["questions"], all_questions)

    return state_with_questions_populated


def submit_action(state, action):
    print("performing `submit_action()` on state: {}, and action: {}".format(state, action))
    action_data = action["data"]
    question_uuid = action_data["uuid"]
    provided_answer = action_data["provided_answer"]

    the_question = next((question for question in state["questions"] if question["uuid"] == question_uuid), None)
    if the_question is None:
        print("Question not found in eligibility or application questions")
        return state

    the_question["provided_answer"] = provided_answer

    # TODO: validate first, then check acceptance criteria

    return state
