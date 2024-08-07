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
import Engine.StateMachine.StateMachine
from Engine.StateMachine.State import State


class DefaultRight(State):
    def __init__(self, state_id):
        super().__init__(state_id)

    def on_load(self, args):
        self.render_surface.sp1.animator.load_animation("default1")

    def on_update(self, args):
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.state_machine.load_state("attack_right")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.state_machine.load_state("run_right")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.state_machine.load_state("run_left")

        if cs.E_PRESSED_BUTTONS in args and args[cs.E_PRESSED_BUTTONS][pygame.K_d]:
            self.state_machine.load_state("run_right")
        if cs.E_PRESSED_BUTTONS in args and args[cs.E_PRESSED_BUTTONS][pygame.K_a]:
            self.state_machine.load_state("run_left")


class DefaultLeft(State):
    def __init__(self, state_id):
        super().__init__(state_id)

    def on_load(self, args):
        self.render_surface.sp1.animator.load_animation("default1")
        self.render_surface.sp1.animator.set_setting(symmetrically_y=True)

    def on_update(self, args):
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.state_machine.load_state("attack_left")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.state_machine.load_state("run_right")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.state_machine.load_state("run_left")
        if cs.E_PRESSED_BUTTONS in args:
            if args[cs.E_PRESSED_BUTTONS][pygame.K_d]:
                self.state_machine.load_state("run_right")
            if args[cs.E_PRESSED_BUTTONS][pygame.K_a]:
                self.state_machine.load_state("run_left")


class AttackRightState(State):
    def __init__(self, state_id):
        super().__init__(state_id)
        self.run = 0

    def on_load(self, args):
        self.run = 0
        self.render_surface.sp1.animator.load_animation("d", playing_cnt=1)

    def on_animation_finished(self, args) -> None:
        if self.run == 1:
            self.state_machine.load_state("run_right")
            return
        elif self.run == -1:
            self.state_machine.load_state("run_left")
            return
        self.state_machine.load_state("default_right")

    def on_update(self, args):
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.run = -1

                if event.key == pygame.K_d:
                    self.run = 1


class AttackLeftState(State):
    def __init__(self, state_id):
        super().__init__(state_id)
        self.run = 0

    def on_load(self, args):
        self.run = 0
        self.render_surface.sp1.animator.load_animation("d", playing_cnt=1)
        self.render_surface.sp1.animator.set_setting(symmetrically_y=True)

    def on_animation_finished(self, args) -> None:
        self.state_machine.load_state("default_left")

    def on_update(self, args):
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.run = -1

                if event.key == pygame.K_d:
                    self.run = 1


class RunRightState(State):
    def __init__(self, state_id):
        super().__init__(state_id)

    def on_load(self, args):
        self.render_surface.sp1.animator.load_animation("run_right")
        # print(pygame.key.ge)

    def on_update(self, args):
        if "tick_length" in args:
            self.render_surface.player.transfer_vector[0] += 200 / self.render_surface.application.fps
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.state_machine.load_state("default_right")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.state_machine.load_state("run_left")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.state_machine.load_state("attack_right")


class RunLeftState(State):
    def __init__(self, state_id):
        super().__init__(state_id)

    def on_load(self, args):
        # self.render_surface.sp1.animator.symmetrically_y = True
        self.render_surface.sp1.animator.load_animation("run_right")
        self.render_surface.sp1.animator.set_setting(symmetrically_y=True)

    def on_update(self, args):
        if "tick_length" in args:
            self.render_surface.player.transfer_vector[0] -= 200 / self.render_surface.application.fps
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.state_machine.load_state("default_left")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.state_machine.load_state("attack_left")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.state_machine.load_state("run_right")


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
        self.display = Engine.RenderSurface.RenderSurface(self, 1, self.width, self.height, np.array([-2000, 0]))
        # self.display.add_border()

        self.state_machine = Engine.StateMachine.StateMachine.StateMachine(self)
        self.player = Engine.RenderSurface.RenderSurface(self.display, 10, 200, 200,
                                                         [self.width // 2 - 100, self.height // 2 - 100])
        self.sp = Engine.SpriteSystem.SingleSprites.SingleSpritesGroup(self.player)
        self.an = Animation(self.application.load_image("_Idle.png", None), 10, 4, "default1")
        self.an2 = Animation(self.application.load_image("_Attack.png"), 4, 12, "attack")
        self.an4 = Animation(self.application.load_image("_AttackComboNoMovement.png"), 10, 12, "d")
        self.an3 = Animation(self.application.load_image("_Run.png"), 10, 12, "run_right")
        self.sp1 = Engine.SpriteSystem.SingleSprites.SingleSprite(None,
                                                                  np.array([200 // 2, 200 // 2]),
                                                                  np.array([None, None]), 2,
                                                                  self.sp)

        self.sp1.animator.add_animation(self.an2)
        self.sp1.animator.add_animation(self.an)
        self.sp1.animator.add_animation(self.an3)
        self.sp1.animator.add_animation(self.an4)
        self.sp1.animator.connect_state_machine(self.state_machine)
        self.state_machine.add_state(DefaultRight("default_right"))
        self.state_machine.add_state(RunRightState("run_right"))
        self.state_machine.add_state(RunLeftState("run_left"))
        self.state_machine.add_state(AttackRightState("attack_right"))
        self.state_machine.add_state(AttackLeftState("attack_left"))
        self.state_machine.add_state(DefaultLeft("default_left"))
        self.state_machine.load_state("default_right")
        self.display.add_border()
        # self.display.fill_color = 'green'
        self.camera1 = Engine.Camera.Camera(self.display, parent_surface=self, render_priority=0, width=self.width,
                                            height=self.height,
                                            transfer_vector=np.array([0, 0]), zoom_restrictions=np.array([2, 0.1]))
        # self.camera1.camera_setting = numpy.array([0, 0, 1,1])
        # self.rect = Engine.BasiсObjects.Polygon(self.display, [], color='green')
        # self.rect.set_geometry(0, self.height // 2 + self.sp1.rect.y // 4, self.width, self.height)
        # self.camera1.camera_setting[2] = 1
        # self.camera1.add_border('red')

        # self.camera1.fill_color= 'red'

    def on_update(self, args):
        # print(pygame.key.get_pressed())aw
        # if "tick_length" in args:
        #     print(1000 / args["tick_length"])
        pass
        # if cs.E_EVENT in args:
        #     event = args[cs.E_EVENT]
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:  # Левая кнопка мыши
        #             self.sp1.animator.load_animation('d', playing_cnt=1)
        #     #         # print(self.sp1.rect, self.sp1.image)
        # self.camera1.camera_motion(event)
        # print(self.camera1.camera_setting[2])


if __name__ == '__main__':
    game = Engine.GameClass.Game((1366, 765), 100, '1', __file__)
    game.register_scene(SecondScene, '1')
    game.register_scene(MainScene, '2')
    game.register_font('Arial', 40, 'arial_40')
    game.set_property(cs.P_SCALING_TYPE, cs.P_SCALING_TYPE_PYGAME)
    game.start()
