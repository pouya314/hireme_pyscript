from typing import List, Dict

from toolz import assoc_in, concat
import requests
import json

from .helpers import get_data, get_root_url
from .constants import QUESTION_CATEGORY_ELIGIBILITY, QUESTION_CATEGORY_APPLICATION
from . import validation_check
from . import acceptance_check


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


def submit_answer_action(state, action):
    print("performing `submit_answer_action()` on state: {}, and action: {}".format(state, action))
    action_data = action["data"]
    question_uuid = action_data["uuid"]
    provided_answer = action_data["provided_answer"]

    the_question = next((question for question in state["questions"] if question["uuid"] == question_uuid), None)
    if the_question is None:
        print("Question not found in eligibility or application questions")
        return state

    the_question["provided_answer"] = provided_answer

    if the_question.get('validations'):
        the_question["validation_errors"] = []
        valid, validation_errors = validation_check.perform(the_question)
        if not valid:
            the_question["validation_errors"] = validation_errors
            return state
    
    if the_question.get('condition'):
        the_question["acceptance_errors"] = []
        accepted, acceptance_error = acceptance_check.perform(the_question)
        if not accepted:
            the_question["acceptance_errors"].append(acceptance_error)
            return state

    return state


def submit_application_action(state, action):
    print("performing `submit_application_action()` on state: {}, and action: {}".format(state, action))
    
    url = f"{get_root_url()}/submit_application"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(state), timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Failed to submit application: {str(e)}")
        return state

    return assoc_in(state, ["application_submitted"], True)
