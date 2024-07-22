import random
import time

import numpy as np
import pygame

import Engine.BasiсObjects
import Engine.RenderSurface
import Engine.GameClass
import Engine.GameScene
import Engine.constants as cs
import Engine.SpriteSystem.MergedSprites
import Engine.SpriteSystem.SingleSprites
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
        # self.sp = Engine.SpriteSystem.MergedSprites.MergedSpritesGroup(self,
        #                                                                self.application.load_image("city.png", -1),
        #                                                                np.array([None, None]),
        #                                                                0.2)
        self.fill_color = 'yellow'

        self.sp2 = Engine.SpriteSystem.SingleSprites.SingleSpritesGroup(self)
        anim1 = Animation(self.application.load_image("_Idle.png"), 10, 4, "stoim")
        anim2 = Animation(self.application.load_image("_Roll.png"), 12, 16, "jump")
        run = Animation(self.application.load_image("_Run.png"), 10, 12, "run")

        self.sp3 = Engine.SpriteSystem.MergedSprites.MergedSpritesGroup(self, anim1, np.array([None, None]), 4)

        sp3_ainmation = Animation(self.application.load_image("_AttackComboNoMovement.png"), 10, 12, "second")
        self.sp3.animator.add_animation(sp3_ainmation)
        self.sp3.animator.add_animation(run)
        self.sp3.animator.add_animation(anim2)
        for i in range(6):
            self.sp1 = Engine.SpriteSystem.MergedSprites.MergedSprite(np.array([i * 200 + 200, 100]), self.sp3)

    def on_update(self, args):
        if "tick_length" in args:
            print(1000 / args["tick_length"])
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.sp3.animator.load_animation('second', playing_cnt=1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.sp3.animator.load_animation('run')
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.sp3.animator.load_default_animation()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.sp3.animator.load_animation('jump', playing_cnt=1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.sp3.animator.load_animation('run')
                self.sp3.animator.symmetrically_x = True
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                self.sp3.animator.load_default_animation()


if __name__ == '__main__':
    game = Engine.GameClass.Game((1366, 765), 100, '1', __file__)
    game.register_scene(SecondScene, '1')
    game.register_scene(MainScene, '2')
    game.register_font('Arial', 40, 'arial_40')
    game.set_property(cs.P_SCALING_TYPE, cs.P_SCALING_TYPE_HYBRID)
    game.start()
