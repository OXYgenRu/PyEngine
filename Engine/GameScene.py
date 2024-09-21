import random

import Engine.RenderSurface
import Engine.CoordsSystem
import numpy as np


#
# class GameScene(Engine.RenderSurface.RenderSurface):
#     def __init__(self, width, height, application):
#         super().__init__(width=width, height=height)
#         self.application = application
#         self.screen_space = Engine.RenderSurface.RenderSurface(self, 1, width, height)
#         self.world_space = Engine.RenderSurface.RenderSurface(self, 0, width, height)

class GameScene(Engine.CoordsSystem.CoordsSystem):
    def __init__(self, application, width, height):
        super().__init__()
        self.application = application
        self.screen_space = Engine.CoordsSystem.CoordsSystem(self, 1, np.array([width // 2, height // 2], float))
        self.world_space = Engine.CoordsSystem.CoordsSystem(self, 0, np.array([width // 2, height // 2], float))
