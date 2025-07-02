from decimal import Decimal
import json
from typing import List, Dict

from jinja2 import Environment, BaseLoader
from pyscript import document
import pydux
import requests
from toolz import assoc_in, concat
from email_validator import validate_email, EmailNotValidError




# ##############################
# #         Constants          #
# ##############################
INITIAL_STATE = {
    "questions": (),
    "application_submitted": False
}

QUESTION_CATEGORY_ELIGIBILITY = "eligibility"
QUESTION_CATEGORY_APPLICATION = "application"
QUESTION_CATEGORIES = (
    QUESTION_CATEGORY_ELIGIBILITY, 
    QUESTION_CATEGORY_APPLICATION
)

VALIDATIONS_REQUIRED = 'required'
VALIDATIONS_IS_STRING = 'is_string'
VALIDATIONS_IS_DECIMAL = 'is_decimal'
VALIDATIONS_IS_EMAIL = 'is_email'

VALIDATIONS = (
    VALIDATIONS_REQUIRED,
    VALIDATIONS_IS_STRING,
    VALIDATIONS_IS_DECIMAL,
    VALIDATIONS_IS_EMAIL
)

CONDITIONS_ANY = 'any'
CONDITIONS_EQUAL = 'equal'
CONDITIONS_GTE = 'gte'

CONDITIONS = (
    CONDITIONS_ANY,
    CONDITIONS_EQUAL,
    CONDITIONS_GTE
)
# ##############################





# ##############################
# #          Errors           #
# ##############################
class ValidationError(Exception):
    pass
# ##############################





# ##############################
# #          Conditions        #
# ##############################
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
# ##############################





# ##############################
# #          Validations       #
# ##############################
def required(provided_answer):
    if not provided_answer:
        raise ValidationError('This field is required.')


def is_string(provided_answer):
    try:
        str(provided_answer)
    except Exception:
        raise ValidationError('This field must be a string.')


def is_decimal(provided_answer):
    try:
        Decimal(provided_answer)
    except Exception:
        raise ValidationError('This field must be a decimal number.')


def is_email(provided_answer):
    try:
        # This validates the email format and also checks for common issues
        validate_email(str(provided_answer), check_deliverability=False)
    except EmailNotValidError as e:
        raise ValidationError('This field must be a valid email address.')
# ##############################





# ##############################
# #          Mappings          #
# ##############################
Validations = {
    VALIDATIONS_REQUIRED: required,
    VALIDATIONS_IS_STRING: is_string,
    VALIDATIONS_IS_DECIMAL: is_decimal,
    VALIDATIONS_IS_EMAIL: is_email
}

Conditions = {
    CONDITIONS_ANY: any,
    CONDITIONS_EQUAL: equal,
    CONDITIONS_GTE: gte
}
# ##############################





# ##############################
# #       Validation Check     #
# ##############################
def perform_validation_check(question):
    """
    Validate the provided answer against the question's validations.
    """
    validation_errors = []
    for validation in question['validations']:
        try:
            Validations[validation](question["provided_answer"])
        except ValidationError as e:
            validation_errors.append(str(e))

    return (False, validation_errors) if validation_errors else (True, ())
# ##############################





# ##############################
# #       Acceptance Check     #
# ##############################
def perform_acceptance_check(question):
    return Conditions[question['condition']](question)
# ##############################





# ##############################
# #          Helpers           #
# ##############################
class Helpers:
    @staticmethod
    def get_root_url():
        return document.getElementById("root-url").innerHTML

    @staticmethod
    def get_data(filename):
        return requests.get(f"{Helpers.get_root_url()}static/data/{filename}").json()

    @staticmethod
    def nofn(questions, current_question):
        same_category_questions = [question for question in questions 
                                   if question["category"] == current_question["category"]]
        idx = same_category_questions.index(current_question)
        return f"{idx + 1}/{len(same_category_questions)}"

    @staticmethod
    def determine_current_question(questions):
        return next((question for question in questions if Helpers.is_question_unanswered_or_not_accepted(question)), None)

    @staticmethod
    def is_question_unanswered_or_not_accepted(question):
        return (Helpers.question_encountered_first_time(question) or 
                Helpers.question_has_validation_errors(question) or 
                Helpers.question_has_acceptance_errors(question))

    @staticmethod
    def question_encountered_first_time(question):
        return question["provided_answer"] is None

    @staticmethod
    def question_has_validation_errors(question):
        return question["validation_errors"] != []

    @staticmethod
    def question_has_acceptance_errors(question):
        return question["acceptance_errors"] != []

    @staticmethod
    def all_questions_answered(questions):
        return all([not Helpers.is_question_unanswered_or_not_accepted(question) for question in questions])

    @staticmethod
    def find_eligibility_questions(questions):
        return [question for question in questions if question["category"] == QUESTION_CATEGORY_ELIGIBILITY]

    @staticmethod
    def find_application_questions(questions):
        return [question for question in questions if question["category"] == QUESTION_CATEGORY_APPLICATION]

    @staticmethod
    def eligibility_wizard_step_css_class_name(questions):
        eligibility_questions = Helpers.find_eligibility_questions(questions)
        if Helpers.all_questions_answered(eligibility_questions):
            return "completed"
        
        current_question = Helpers.determine_current_question(questions)
        if current_question and current_question in eligibility_questions:
            return "active"
        
        return "upcoming"

    @staticmethod
    def application_wizard_step_css_class_name(questions):
        application_questions = Helpers.find_application_questions(questions)
        if Helpers.all_questions_answered(application_questions):
            return "completed"
        
        current_question = Helpers.determine_current_question(questions)
        if current_question and current_question in application_questions:
            return "active"
        
        return "upcoming"

    @staticmethod
    def review_and_submit_wizard_step_css_class_name(questions, application_submitted):
        if Helpers.all_questions_answered(questions):
            if application_submitted:
                return "completed"
            else:
                return "active"            
        
        return "upcoming"
# ##############################





# ##############################
# #          Actions           #
# ##############################
def initialize_action(state, action):
    print("performing `initialize_action()` on state: {}".format(state))

    eligibility_questions: List[Dict] = [
        assoc_in(question, ["category"], QUESTION_CATEGORY_ELIGIBILITY) 
        for question in Helpers.get_data("questions.json")
    ]
    application_questions: List[Dict] = [
        assoc_in(question, ["category"], QUESTION_CATEGORY_APPLICATION) 
        for question in Helpers.get_data("application.json")
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
        valid, validation_errors = perform_validation_check(the_question)
        if not valid:
            the_question["validation_errors"] = validation_errors
            return state
    
    if the_question.get('condition'):
        the_question["acceptance_errors"] = []
        accepted, acceptance_error = perform_acceptance_check(the_question)
        if not accepted:
            the_question["acceptance_errors"].append(acceptance_error)
            return state

    return state


def submit_application_action(state, action):
    print("performing `submit_application_action()` on state: {}, and action: {}".format(state, action))
    
    url = f"{Helpers.get_root_url()}/submit_application"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(state), timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Failed to submit application: {str(e)}")
        return state

    return assoc_in(state, ["application_submitted"], True)
# ##############################





# ##############################
# #          Reducers          #
# ##############################
def reducer(state, action):
    print(f"handling action: {action}, state: {state}")
    if state is None:
        state = INITIAL_STATE
    if action is None:
        return state
    elif action["type"] == "INITIALIZE":
        return initialize_action(state, action)
    elif action["type"] == "SUBMIT_ANSWER":
        return submit_answer_action(state, action)
    elif action["type"] == "SUBMIT_APPLICATION":
        return submit_application_action(state, action)
    print(f"Action handler returning state: {state}")
    return state
# ##############################





# ##############################
# #          UI Renderer       #
# ##############################
def render_ui(state):
    print(f"render_ui() called with state: {state}")

    wizard_template_string = document.getElementById("wizard-template").innerHTML

    rtemplate = Environment(loader=BaseLoader()).from_string(wizard_template_string)
    rendered_html = rtemplate.render(helpers=Helpers, **state)

    wizard_container = document.getElementById("wizard-container")
    wizard_container.innerHTML = rendered_html
# ##############################





# ##############################
# #        Pydux Store         #
# ##############################
store = pydux.create_store(reducer)
store.subscribe(lambda: render_ui(store.get_state()))
store.dispatch({"type": "INITIALIZE"})

def submit_answer_clicked(e):
    form = e.target.form
    form_data = {
        element.name: element.value 
        for element in form.elements 
        if element.name
    }
    
    print(f"Form data: {form_data}")
    store.dispatch({
        "type": "SUBMIT_ANSWER",
        "data": form_data
    })


def submit_application_clicked(e):
    store.dispatch({"type": "SUBMIT_APPLICATION"})
# ##############################
