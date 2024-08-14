import os
import sys

import numpy
import pygame
import shapely

from Engine.tools import scale_image, polygon_converter, render_surface_convertor, surface_convertor


class Shape:
    def __init__(self):
        self.points = numpy.array([])

    def update(self, args):
        pass

    def move(self, transfer_vector: numpy.array):
        self.points += transfer_vector


class Polygon(Shape):
    def __init__(self, render_surface, points: numpy.array = numpy.array([[0, 0], [0, 0], [0, 0], [0, 0]]), color='red',
                 width=0):
        super().__init__()
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.width = width
        self.render_surface.add_content(self)

    def render(self, matrix: numpy.array = None):
        new_points = polygon_converter(self.points, matrix)
        width = self.width
        if matrix is not None:
            width = self.width * matrix[8]
        if self.width != 0:
            width = max(1, width)
        pygame.draw.polygon(self.render_surface, self.color, new_points.tolist(), int(width))

    def set_geometry(self, x1, y1, x2, y2):
        self.points = numpy.array(
            [[x1, y1], [x2 + x1, y1], [x2 + x1, y2 + y1], [x1, y2 + y1]])


class Circle(Shape):
    def __init__(self, render_surface, points: numpy.array, color='red', width=0):
        super().__init__()
        self.render_surface = render_surface
        self.points = points
        self.color = color
        self.width = width
        self.render_surface.add_content(self)

    def render(self, matrix: numpy.array = None):
        new_points = polygon_converter(self.points, matrix)
        width = self.width
        if matrix is not None:
            width = self.width * matrix[8]
        if self.width != 0:
            width = max(1, width)
        pygame.draw.circle(self.render_surface, self.color, new_points[0], new_points[1][0] - new_points[0][0],
                           int(width))


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

    def render(self, matrix: numpy.array = None):
        text_surface = self.render_surface.application.font_storage[self.font_id].render(self.text, True, self.color)
        self.render_surface.blit(surface_convertor(self.points, text_surface, matrix), self.points.tolist())
