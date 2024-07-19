import pydux

from .reducers import reducer
from .ui import render_ui

store = pydux.create_store(reducer)
store.subscribe(lambda: render_ui(store.get_state()))
store.dispatch({'type': 'INITIALIZE'})


def submit_button_clicked(e):
    store.dispatch({'type': 'SUBMIT'})
