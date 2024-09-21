import numpy
import pygame

from Engine.Animations.Animation import Animation
from Engine.Animations.Animator import Animator
from Engine.tools import scale_image, surface_convertor, polygon_converter
import Engine.constants as cs


class SpriteSource:
    def __init__(self, application, image_or_animation, size: numpy.array, scale):
        self.application = application
        self.animator = Animator(self.application, image_or_animation, size, scale)
        self.sprites = []
        self.image = self.animator.get_current_frame()
        self.rendered_image = self.animator.get_current_frame()
        self.matrix = None
        self.image_to_update = False
        self.event_id = -1

    def update(self, event_list, event_id):
        # print(2)
        if event_id == self.event_id:
            return
        self.event_id = event_id
        self.animator.update(event_list, event_id)
        self.image_to_update = False
        for event in event_list:
            if event[0] == cs.E_EVENT:
                if pygame.USEREVENT + self.animator.event_number == event[1].type:
                    self.image = self.animator.get_frame()
                    self.image_to_update = True
                if cs.E_START_NEW_ANIMATION == event[1].type:
                    self.image = self.animator.get_frame()
                    self.image_to_update = True

    def update_image(self, matrix: numpy.array):

        if self.matrix is None or matrix is None:
            self.matrix = matrix
            new_surface = surface_convertor(numpy.array([0, 0]), self.image, matrix, self.application)
            if new_surface[0] is True:
                self.rendered_image = new_surface[2]
            self.image_to_update = False
        elif matrix[8] != self.matrix[8] or self.image_to_update:
            self.matrix = matrix
            new_surface = surface_convertor(numpy.array([0, 0]), self.image, matrix, self.application)
            if new_surface[0] is True:
                self.rendered_image = new_surface[2]
            self.image_to_update = False

    def resize(self, size: numpy.array = None, scale=None):
        self.animator.resize(size, scale)
        self.image_to_update = True


class Sprite(pygame.sprite.Sprite):
    def __init__(self, render_surface, sprite_source, point: numpy.array):
        super().__init__()
        self.rect = None
        self.point = point
        self.render_surface = render_surface
        self.sprite_source = sprite_source
        self.sprite_source.sprites.append(self)
        self.application = render_surface.application
        self.render_surface.add_content(self)
        self.image = self.sprite_source.image
        self.update_collision()

    def render(self, matrix: numpy.array = None, custom_surface=None):
        self.sprite_source.update_image(matrix)
        self.image = self.sprite_source.rendered_image
        self.update_collision()
        point = polygon_converter(numpy.array([self.point]), matrix)[0]
        if custom_surface is not None:
            custom_surface.blit(self.image, point.tolist())
        else:
            self.render_surface.blit(self.image, point.tolist())

    def resize(self, size: numpy.array = None, scale=None):
        self.sprite_source.resize(size, scale)

    def update(self, event_list, event_id):
        self.sprite_source.update(event_list, event_id)
        self.on_update(event_list, event_id)

    def on_update(self, args, event_id):
        pass

    def update_collision(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.point[0] - self.rect.width // 2
        self.rect.y = self.point[1] - self.rect.height // 2

# class Sprite(pygame.sprite.Sprite):
#     def __init__(self, coords_system, image_or_animation, point: numpy.array, size: numpy.array, render_scale):
#         super().__init__()
#         self.rect = None
#         self.coords_system = coords_system
#         self.application = coords_system.application
#         self.coords_system.add_content(self)
#         self.animator = Animator(self.application, image_or_animation, size, render_scale)
#         self.image = self.animator.get_current_frame()
#         self.point = point
#         self.in_sprite_union: bool = False
#         self.sprite_union = None
#         self.update_collision()
#
#     def render(self, matrix: numpy.array = None, custom_surface=None):
#         sprite = surface_convertor(self.point, self.image, matrix, self.application)
#         if custom_surface is not None:
#             custom_surface.blit(sprite[1], sprite[0].tolist())
#         else:
#             self.coords_system.blit(sprite[1], sprite[0].tolist())
#
#     def resize(self, size: numpy.array = None, render_scale=None):
#         self.animator.resize(size, render_scale)
#         self.image = self.animator.get_current_frame()
#         self.update_collision()
#
#     def update_collision(self):
#         self.rect = self.image.get_rect()
#         self.rect.x = self.point[0] - self.rect.width // 2
#         self.rect.y = self.point[1] - self.rect.height // 2
#
#     def update(self, args):
#         self.animator.update(args)
#         if cs.E_EVENT in args:
#             if pygame.USEREVENT + self.animator.event_number == args[cs.E_EVENT].type:
#                 self.image = self.animator.get_frame()
#                 self.update_collision()
#             if cs.E_START_NEW_ANIMATION == args[cs.E_EVENT].type:
#                 self.image = self.animator.get_frame()
#                 self.update_collision()
#
#     def on_update(self, args):
#         pass


# class SpritesUnion:
#     def __init__(self):
