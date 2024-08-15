import random

import Engine.RenderSurface


class GameScene(Engine.RenderSurface.RenderSurface):
    def __init__(self, width, height, application):
        super().__init__(width=width, height=height)
        self.application = application
        self.screen_space = Engine.RenderSurface.RenderSurface(self, 1, width, height)
        self.world_space = Engine.RenderSurface.RenderSurface(self, 0, width, height)
