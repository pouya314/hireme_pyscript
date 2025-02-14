from jinja2 import Environment, BaseLoader
from pyscript import document
from . import helpers


def render_ui(state):
    print(f"render_ui() called with state: {state}")

    wizard_template_string = document.getElementById("wizard-template").innerHTML

    rtemplate = Environment(loader=BaseLoader()).from_string(wizard_template_string)
    rendered_html = rtemplate.render(helpers=helpers, **state)

    wizard_container = document.getElementById("wizard-container")
    wizard_container.innerHTML = rendered_html
