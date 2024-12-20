import math
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
from Engine.CoordsSystem import CoordsSystem
from Engine.StateMachine.State import State
import Engine.CameraV2
from Engine.Colliders.UICollider import UICollider
from Engine.SpriteSystem.Sprite import Sprite, SpriteSource
from ExampleGame.start_scene import Menu
from Engine.CameraV3 import Camera


class FPSMeter(Engine.RenderSurface.RenderSurface):
    def __init__(self, parent_surface=None, render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = numpy.array([0, 0])):
        super().__init__(parent_surface, render_priority, width, height, transfer_vector)
        self.fps = Engine.BasiсObjects.Text(self, np.array([0, 0]), "0", color='green')

    def on_update(self, event_list, event_id):
        for event in event_list:
            if event[0] == cs.E_TICK_LENGTH:
                self.fps.text = str(1000 / event[1])


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
        pass


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
        pass


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
        # self.coords_system.sp1.animator.symmetrically_y = True
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

        self.fps_meter = FPSMeter(self.screen_space, 2, 50, 25)

        self.camera = Engine.CameraV2.Camera(self.world_space, parent_surface=self.screen_space, render_priority=0,
                                             width=width,
                                             height=height)
        self.text = Engine.BasiсObjects.Text(self.screen_space, np.array([0, 0]), "rrr")
        self.world_space.set_filling('yellow')
        self.camera.set_filling('yellow')
        self.an = Animation(self.application.load_image("_Idle.png", None), 10, 4, "default1")
        self.slepa = Engine.SpriteSystem.Sprite.SpriteSource(self.application, self.an,
                                                             np.array([None, None]), 1)

        for i in range(0, 50):
            for j in range(0, 50):
                # new_surface = Engine.RenderSurface.RenderSurface(self.world_space, 0, 50, 50,
                #                                                  np.array([i * 60, j * 60]))
                # new_surface.set_filling('green')
                # new_surface.test = 0

                #    self.button.rotation_pos = numpy.array([-2, 0])

                Engine.SpriteSystem.Sprite.Sprite(self.world_space, self.slepa, np.array([i * 30, j * 30]))

    def uu(self):
        self.rect1.color = 'blue'

    def uu1(self):
        self.rect1.color = 'green'

    def uu2(self, a):
        self.camera.set_filling((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def u3(self):
        self.button.angle += 10

    def on_update(self, args, event_id):
        # print(self.camera.camera_setting.tolist())
        # if "tick_length" in args:
        #     print(1000 / args["tick_length"])
        pass


class SecondScene(Engine.GameScene.GameScene):
    def __init__(self, application, width, height):
        super().__init__(width=width, height=height, application=application)
        self.camera = Camera(self.screen_space, 0, target=self.world_space)
        # self.world_space.angle = 40
        self.world_space.set_visible_off()
        # self.world_space = Engine.RenderSurface.RenderSurface(self, 1, self.width, self.height, np.array([-20000, -5000]))
        # self.world_space.add_border()
        self.rect = Engine.BasiсObjects.Polygon(self.world_space, [], 'green', width=10)
        self.rect.set_geometry(0, 100, 100, 100)
        # self.world_space.test = 1
        self.state_machine = Engine.StateMachine.StateMachine.StateMachine(self)
        self.player = Engine.RenderSurface.RenderSurface(self.world_space, 10, 200, 200,
                                                         [self.width // 2 - 100, self.height // 2 - 100])
        # self.player
        self.player.add_border("green")
        self.player.set_filling('red')

        self.an2 = Animation(self.application.load_image("_Attack.png"), 4, 12, "attack")
        self.an4 = Animation(self.application.load_image("_AttackComboNoMovement.png"), 10, 12, "d")
        self.an3 = Animation(self.application.load_image("_Run.png"), 10, 12, "run_right")
        self.sp1 = Engine.SpriteSystem.SingleSprites.SingleSprite(None,
                                                                  np.array([200 // 2, 200 // 2]),
                                                                  np.array([None, None]), 1 )

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
        self.world_space.add_border()

        # self.world_space.fill_color = 'green'

        # self.camera1.camera_setting = numpy.array([0, 0, 1,1])
        # self.rect = Engine.BasiсObjects.Polygon(self.world_space, [], color='green')
        # self.rect.set_geometry(0, self.height // 2 + self.sp1.rect.y // 4, self.width, self.height)
        # self.camera1.camera_setting[2] = 1
        # self.camera1.add_border('red')

        # self.camera1.fill_color= 'red'

    def on_update(self, args):
        # print(pygame.key.get_pressed())aw
        if "tick_length" in args:
            print(1000 / args["tick_length"])
        # pass
        # print(self.world_space.camera_setting, self.world_space2.camera_setting)
        # if cs.E_EVENT in args:
        #     event = args[cs.E_EVENT]
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:  # Левая кнопка мыши
        #             self.sp1.animator.load_animation('d', playing_cnt=1)
        #     #         # print(self.sp1.rect, self.sp1.image)
        # self.camera1.camera_motion(event)
        # print(self.camera1.camera_setting[2])

    # def point_calculations_world_spaceed_coords(point, camera_object):
    #     x = WIDTH // 2 - (camera_object.camera_pos[0] + point.p_x + camera_object.moving_vector[0])
    #     x *= camera_object.camera_zoom
    #     x = WIDTH // 2 - x
    #
    #     y = HEIGHT // 2 - (camera_object.camera_pos[1] + point.p_y + camera_object.moving_vector[1])
    #     y *= camera_object.camera_zoom
    #     y = HEIGHT // 2 - y
    #
    #     visual_point = (x, y)
    #     return visual_point


class TestScene(Engine.GameScene.GameScene):
    def __init__(self, application, width, height):
        super().__init__(application, width, height)


    def on_update(self, event_list, event_id):
        for event in event_list:
            if event[0] == cs.E_TICK_LENGTH:
                print(1000 / event[1])
        # self.s1.angle += 0.01
        # self.s2.angle -= 1
        # self.angle += 1
        self.camera.camera_angle += 1
        # x = self.screen_space.angle
        # print(self.screen_space.position, np.array([math.sin(x), math.cos(x)], float))
        # self.screen_space.position += np.array([math.sin(x / 10) * 10, math.cos(x / 10) * 10], float)
        # for event in event_list:
        #     if event[0] == cs.E_EVENT and event[1].type == pygame.MOUSEMOTION:
        #         x = event[1].pos[0] - self.screen_space.position.tolist()[0]
        #         y = event[1].pos[1] - self.screen_space.position.tolist()[1]
        #         self.screen_space.angle = -math.degrees(math.atan2(y, x))
        # # self.shape.move(numpy.array([-self.screen_space.angle * 0.1, 0], float))
        # # self.screen_space.angle += 1
        # self.screen_space.render_scale = 0.1
        # self.screen_space.render_transfer_vector = numpy.array([-500, 100])
        # self.screen_space.angle = 10
        pass


if __name__ == '__main__':
    game = Engine.GameClass.Game((1366, 765), 100, '1', __file__)
    game.register_scene(TestScene, '1')
    # game.register_scene(Menu, 'menu')
    # game.register_scene(MainScene, '2')
    game.register_font('Arial', 40, 'arial_40')
    game.set_property(cs.P_SCALING_TYPE, cs.P_SCALING_TYPE_PYGAME)
    game.start()
