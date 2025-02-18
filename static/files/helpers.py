import requests
from pyscript import document


def get_root_url():
    return document.getElementById("root-url").innerHTML


def get_data(filename):
    return requests.get(f"{get_root_url()}static/data/{filename}").json()


def determine_current_question(questions):
    # if any(question_has_acceptance_errors(question) for question in questions):
    #     return None

    return next((question for question in questions if not_answered(question)), None)


# TODO: rename this
def not_answered(question):
    return (question_encountered_first_time(question) or 
            question_has_validation_errors(question) or 
            question_has_acceptance_errors(question))


def question_encountered_first_time(question):
    return question["provided_answer"] is None


def question_has_validation_errors(question):
    return question["validation_errors"] != []


def question_has_acceptance_errors(question):
    return question["acceptance_errors"] != []
