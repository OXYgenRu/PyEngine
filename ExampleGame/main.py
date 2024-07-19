import random
import time

import numpy as np
import pygame

import Engine.BasiсObjects
import Engine.RenderSurface
import Engine.GameClass
import Engine.GameScene
import Engine.constants as cs


# class CustomSprite(Engine.BasiсObjects.Sprite):
#     def __init__(self):


class MainScene(Engine.GameScene.GameScene):
    def __init__(self, width, height, application):
        super().__init__(width=width, height=height, application=application)
        self.pl = Engine.BasiсObjects.Polygon(self, np.array([[100, 100], [200, 100], [200, 200], [100, 200]]))
        self.surf = Engine.RenderSurface.RenderSurface(self, 2, 200, 200, np.array([100, 200]))
        self.pl1 = Engine.BasiсObjects.Polygon(self.surf, np.array([[50, 50], [100, 50], [200, 100], [50, 200]]))
        self.pl1.color = 'green'
        self.surf2 = Engine.RenderSurface.RenderSurface(self, 1, 600, 600, np.array([-200, -200]))
        self.pl12 = Engine.BasiсObjects.Polygon(self.surf2,
                                                np.array([[400, 400], [600, 400], [600, 600], [400, 600]]))
        self.pl12.color = 'blue'


class SecondScene(Engine.GameScene.GameScene):
    def __init__(self, width, height, application):
        super().__init__(width=width, height=height, application=application)
        # self.fill_color = 'red'
        # self.sr1 = Engine.RenderSurface.RenderSurface(self, 2, 200, 200, np.array([100, 100]))
        # self.sr2 = Engine.RenderSurface.RenderSurface(self, 3, 200, 200, np.array([150, 100]))
        # self.sr1.add_border()
        # self.sr2.add_border()
        # # self.sr2.hide()
        # self.cr = Engine.BasiсObjects.Circle(self.sr1, np.array([[100, 100], [150, 150]]))
        # self.tx = Engine.BasiсObjects.Text(self.sr2, np.array([100, 100]),
        #                                   'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', font_id='arial_40',
        self.sp = Engine.BasiсObjects.MergedSpritesGroup(self, self.application.load_image("city.png", None),
                                                         np.array([None, None]),
                                                         0.2)
        self.fill_color = 'yellow'
        for i in range(6):
            self.sp1 = Engine.BasiсObjects.Sprite(np.array([i * 100, 100]), self.sp)

    def update(self, args):
        self.sp.resize_image(np.array([None, None]), random.uniform(0.2, 0.3))


if __name__ == '__main__':
    game = Engine.GameClass.Game((1366, 765), 10, '1', __file__)
    game.register_scene(SecondScene, '1')
    game.register_scene(MainScene, '2')
    game.register_font('Arial', 40, 'arial_40')
    game.set_property(cs.P_SCALING_TYPE, cs.P_SCALING_TYPE_HYBRID)
    game.start()
