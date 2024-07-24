import numpy
import pygame

from Engine.Animations.Animation import Animation
from Engine.Animations.Animator import Animator
from Engine.tools import scale_image
import Engine.constants as cs


class SingleSpritesGroup(pygame.sprite.Group):
    def __init__(self, render_surface):
        super().__init__()
        self.render_surface = render_surface
        self.application = render_surface.application
        self.render_surface.add_content(self)

    def render(self):
        self.draw(self.render_surface)


class SingleSprite(pygame.sprite.Sprite):
    def __init__(self, image_or_animation, point: numpy.array, size: numpy.array, scale, group):
        super().__init__(group)
        self.rect = None
        self.application = group.application
        self.animator = Animator(self.application, image_or_animation, size, scale)
        self.image = self.animator.get_current_frame()
        self.point = point
        self.update_collision()

    def resize(self, size: numpy.array = None, scale=None):
        self.animator.resize(size, scale)

        self.image = self.animator.get_current_frame()
        self.update_collision()

    def update_collision(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.point[0] - self.rect.width // 2
        self.rect.y = self.point[1] - self.rect.height // 2

    def update(self, args):
        self.animator.update(args)
        if cs.E_EVENT in args:
            if pygame.USEREVENT + self.animator.event_number == args[cs.E_EVENT].type:
                self.image = self.animator.get_frame()
                self.update_collision()
            if cs.E_START_NEW_ANIMATION == args[cs.E_EVENT].type:
                self.image = self.animator.get_frame()
                self.update_collision()

    def on_update(self, args):
        pass
