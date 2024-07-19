import os
import sys

import numpy
import pygame
import shapely

from Engine.tools import scale_image


class Shape:
    def __init__(self):
        self.points = numpy.array([])

    def update(self, args):
        pass

    def move(self, transfer_vector: numpy.array):
        self.points += transfer_vector


class Polygon(Shape):
    def __init__(self, render_surface, points: numpy.array, color='red', width=0):
        super().__init__()
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.width = width
        self.render_surface.add_content(self)

    def render(self):
        pygame.draw.polygon(self.render_surface, self.color, self.points.tolist(), self.width)

    def set_geometry(self, x1, y1, x2, y2):
        cnt = 20
        self.points = numpy.array(
            [[x1 * cnt, y1 * cnt], [x2 * cnt, y1 * cnt], [x2 * cnt, y2 * cnt], [x1 * cnt, y2 * cnt]])


class Circle(Shape):
    def __init__(self, render_surface, points: numpy.array, color='red', width=0):
        super().__init__()
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.width = width
        self.render_surface.add_content(self)

    def render(self):
        pygame.draw.circle(self.render_surface, self.color, self.points[0], self.points[1][0] - self.points[0][0],
                           self.width)


class Text(Shape):
    def __init__(self, render_surface, points: numpy.array, text, color='red', font_id='arial_23'):
        super().__init__()
        if type(points) == list:
            points = numpy.array(points)
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.font_id = font_id
        self.text = text
        self.render_surface.add_content(self)

    def render(self):
        text_surface = self.render_surface.application.font_storage[self.font_id].render(self.text, True, self.color)
        self.render_surface.blit(text_surface, self.points.tolist())


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


class SingleSpritesGroup(pygame.sprite.Group):
    def __init__(self, render_surface):
        super().__init__()
        self.render_surface = render_surface
        self.application = render_surface.application
        self.render_surface.add_content(self)

    def render(self):
        self.draw(self.render_surface)


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


class SingleSprite(pygame.sprite.Sprite):
    def __init__(self, image, point: numpy.array, size: numpy.array, scale, group):
        super().__init__(group)
        self.original_image = image
        self.application = group[0].application
        self.image = scale_image(self.application, self.original_image, size, scale)
        self.rect = self.image.get_rect()
        self.rect.x = point[0] - self.rect.width // 2
        self.rect.y = point[1] - self.rect.height // 2

    def resize(self, size: numpy.array = None, scale=None):
        self.image = scale_image(self.application, self.original_image, size, scale)
