import random

import Engine.RenderSurface


class GameScene(Engine.RenderSurface.RenderSurface):
    def __init__(self, width, height, application):
        super().__init__(width=width, height=height)
        self.application = application

    def update(self, args):
        print(1000 / args["tick_length"])
