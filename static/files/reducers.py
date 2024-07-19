from .actions import initialize_action, submit_action
from .constants import INITIAL_STATE


def reducer(state, action):
    print(f'handling action: {action}, state: {state}')
    if state is None:
        state = INITIAL_STATE
    if action is None:
        return state
    elif action['type'] == 'INITIALIZE':
        return initialize_action(state, action)
    elif action['type'] == 'SUBMIT':
        return submit_action(state, action)
    print(f'Action handler returning state: {state}')
    return state
