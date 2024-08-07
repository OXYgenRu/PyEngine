class State:
    def __init__(self, state_id):
        self.state_id = state_id
        self.state_machine = None
        self.render_surface = None

    def update(self, args):
        self.on_update(args)

    def on_update(self, args):
        pass

    def load(self, args):
        self.on_load(args)

    def on_load(self, args):
        pass

    def animation_finished(self, args):
        self.on_animation_finished(args)

    def on_animation_finished(self, args):
        pass
