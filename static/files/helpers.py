import requests
from pyscript import document

from .constants import QUESTION_CATEGORY_ELIGIBILITY, QUESTION_CATEGORY_APPLICATION


def get_root_url():
    return document.getElementById("root-url").innerHTML


def get_data(filename):
    return requests.get(f"{get_root_url()}static/data/{filename}").json()


def determine_current_question(questions):
    return next((question for question in questions if is_question_unanswered_or_not_accepted(question)), None)


def is_question_unanswered_or_not_accepted(question):
    return (question_encountered_first_time(question) or 
            question_has_validation_errors(question) or 
            question_has_acceptance_errors(question))


def question_encountered_first_time(question):
    return question["provided_answer"] is None


def question_has_validation_errors(question):
    return question["validation_errors"] != []


def question_has_acceptance_errors(question):
    return question["acceptance_errors"] != []


def all_questions_answered(questions):
    return all([not is_question_unanswered_or_not_accepted(question) for question in questions])


def find_eligibility_questions(questions):
    return [question for question in questions if question["category"] == QUESTION_CATEGORY_ELIGIBILITY]


def find_application_questions(questions):
    return [question for question in questions if question["category"] == QUESTION_CATEGORY_APPLICATION]


def eligibility_wizard_step_css_class_name(questions):
    eligibility_questions = find_eligibility_questions(questions)
    if all_questions_answered(eligibility_questions):
        return "completed"
    
    current_question = determine_current_question(questions)
    if current_question and current_question in eligibility_questions:
        return "active"
    
    return "upcoming"


def application_wizard_step_css_class_name(questions):
    application_questions = find_application_questions(questions)
    if all_questions_answered(application_questions):
        return "completed"
    
    current_question = determine_current_question(questions)
    if current_question and current_question in application_questions:
        return "active"
    
    return "upcoming"


def review_and_submit_wizard_step_css_class_name(questions, application_submitted):
    if all_questions_answered(questions):
        if application_submitted:
            return "completed"
        else:
            return "active"            
    
    return "upcoming"
