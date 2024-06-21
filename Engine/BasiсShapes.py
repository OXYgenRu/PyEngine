import numpy
import pygame
import shapely


class Polygon:
    def __init__(self, render_surface, points: numpy.array, color='red', width=0):
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.width = width
        self.render_surface.add_content(self)

    def render(self):
        pygame.draw.polygon(self.render_surface, self.color, self.points.tolist(), self.width)


class Circle:
    def __init__(self, render_surface, points: numpy.array, color='red', width=0):
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.width = width
        self.render_surface.add_content(self)

    def render(self):
        pygame.draw.circle(self.render_surface, self.color, self.points[0], self.points[1][0] - self.points[0][0],
                           self.width)


class Text:
    def __init__(self, render_surface, point: numpy.array, text, color='red', font_id='arial_23'):
        self.render_surface = render_surface
        self.point = point
        self.color = color
        self.font_id = font_id
        self.text = text
        self.render_surface.add_content(self)

    def render(self):
        text_surface = self.render_surface.application.font_storage[self.font_id].render(self.text, True, self.color)
        self.render_surface.blit(text_surface, self.point.tolist())
