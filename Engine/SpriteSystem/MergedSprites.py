import numpy
import pygame

from Engine.tools import scale_image


class MergedSpritesGroup(pygame.sprite.Group):
    def __init__(self, render_surface, image, size: numpy.array = None, scale=None):
        super().__init__()
        self.render_surface = render_surface
        self.application = render_surface.application
        self.original_image = image
        self.image = scale_image(self.application, self.original_image, size, scale)
        self.render_surface.add_content(self)

    def render(self):
        self.draw(self.render_surface)

    def resize_image(self, size: numpy.array = None, scale=None):
        self.image = scale_image(self.application, self.original_image, size, scale)
        for sprite in self.sprites():
            sprite.resize(self.image)


class MergedSprite(pygame.sprite.Sprite):
    def __init__(self, point: numpy.array, group):
        super().__init__(group)
        self.image = group.image
        self.point = point
        self.application = group.application
        self.rect = self.image.get_rect()
        self.rect.x = point[0] - self.rect.width // 2
        self.rect.y = point[1] - self.rect.height // 2

    def resize(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.point[0] - self.rect.width // 2
        self.rect.y = self.point[1] - self.rect.height // 2
