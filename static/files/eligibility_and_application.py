import pydux

from .reducers import reducer
from .ui import update_user_interface

wizard = pydux.create_store(reducer)
wizard.subscribe(lambda: update_user_interface(wizard.get_state()))
wizard.dispatch({'type': 'INITIALIZE'})


def submit_button_clicked(e):
    wizard.dispatch({'type': 'SUBMIT'})
