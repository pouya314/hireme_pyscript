from __future__ import print_function
import pydux


def counter(state, action):
    if state is None:
        state = 0
    if action is None:
        return state
    elif action['type'] == 'INCREMENT':
        return state + 1
    elif action['type'] == 'DECREMENT':
        return state - 1
    return state


store = pydux.create_store(counter)

store.subscribe(lambda: print(f"store => {store.get_state()}"))
