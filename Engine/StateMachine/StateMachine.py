from collections import defaultdict

import Engine.StateMachine.State


class StateMachine:
    def __init__(self, render_surface):
        self.state: Engine.StateMachine.State = None
        self.render_surface = render_surface
        self.states = defaultdict(None)
        self.render_surface.add_updating_content(self)

    def add_state(self, new_state: Engine.StateMachine.State.State):
        self.states[new_state.state_id] = new_state
        self.states[new_state.state_id].state_machine = self
        self.states[new_state.state_id].render_surface = self.render_surface

    def load_state(self, state_id):
        self.state = self.states[state_id]
        self.state.load({})

    def update(self, args):
        self.state.update(args)

    def animation_finished(self, args):
        self.state.animation_finished(args)
