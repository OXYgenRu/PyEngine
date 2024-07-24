import random
import time

import numpy
import numpy as np
import pygame

import Engine.BasiсObjects
import Engine.RenderSurface
import Engine.GameClass
import Engine.GameScene
import Engine.constants as cs
import Engine.SpriteSystem.MergedSprites
import Engine.SpriteSystem.SingleSprites
import Engine.Camera
from Engine.Animations.Animation import Animation


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
        self.display = Engine.RenderSurface.RenderSurface(self, 1, 400, 400, np.array([50, 100]))
        self.display.add_border()
        self.sp = Engine.SpriteSystem.SingleSprites.SingleSpritesGroup(self.display)
        self.an = Animation(self.application.load_image("tree.png", None), 1, 24, "default")
        self.sp1 = Engine.SpriteSystem.SingleSprites.SingleSprite(self.an,
                                                                  np.array([200, 200]), 0, 0.5,
                                                                  self.sp)
        # self.display.fill_color = 'green'
        self.camera1 = Engine.Camera.Camera(self.display, parent_surface=self, render_priority=0, width=500,
                                            height=500,
                                            transfer_vector=np.array([600, 200]))
        # self.camera1.camera_setting = numpy.array([0, 0, 1,1])
        self.camera1.add_border('red')
        # self.camera1.fill_color= 'red'

    def on_update(self, args):
        # if "tick_length" in args:
        #     print(1000/args["tick_length"])
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.sp1.animator.resize(scale=self.sp1.animator.scale + 0.1)
                    # print(self.sp1.rect, self.sp1.image)
            self.camera1.camera_motion(event)
            # print(self.camera1.camera_setting[2])


if __name__ == '__main__':
    game = Engine.GameClass.Game((1366, 765), 100, '1', __file__)
    game.register_scene(SecondScene, '1')
    game.register_scene(MainScene, '2')
    game.register_font('Arial', 40, 'arial_40')
    game.set_property(cs.P_SCALING_TYPE, cs.P_SCALING_TYPE_PYGAME)
    game.start()
