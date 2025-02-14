import pydux

from .reducers import reducer
from .ui import render_ui

store = pydux.create_store(reducer)
store.subscribe(lambda: render_ui(store.get_state()))
store.dispatch({"type": "INITIALIZE"})


def submit_button_clicked(e):
    form = e.target.form
    form_data = {
        element.name: element.value 
        for element in form.elements 
        if element.name
    }
    print(f"Form data: {form_data}")
    store.dispatch({
        "type": "SUBMIT",
        "data": form_data
    })
