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
