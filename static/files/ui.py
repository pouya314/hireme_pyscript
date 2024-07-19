from pyscript import document

from .helpers import get_root_url


def update_user_interface(state):
    print(f'update_user_interface() called with state: {state}')
    root_url_val = get_root_url()

    wizard_element = document.getElementById("wizard-container")
    wizard_element.innerHTML = root_url_val

    # fact_tpl_element = document.getElementById("facts-template")
    # fact_tpl_str = fact_tpl_element.innerHTML
    #
    # rtemplate = Environment(loader=BaseLoader()).from_string(fact_tpl_str)
    # rendered_facts = rtemplate.render(**state)
    #
    # result_element = document.getElementById("facts-container")
    # result_element.innerHTML = rendered_facts
