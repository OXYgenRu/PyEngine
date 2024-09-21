import os
import sys

import numpy
import numpy as np
import pygame
import shapely

from Engine.RenderSystem.RenderInput import RenderInput
from Engine.tools import scale_image, polygon_converter, render_surface_convertor, surface_convertor


class Shape:
    def __init__(self):
        self.points = numpy.array([])

    def update(self, args, event_id):
        pass

    def move(self, transfer_vector: numpy.array):
        self.points += transfer_vector


class Polygon(Shape):
    def __init__(self, coords_system, points: numpy.array = numpy.array([[0, 0], [0, 0], [0, 0], [0, 0]], float),
                 color='red',
                 width=0):
        super().__init__()
        self.coords_system = coords_system
        self.points = points
        self.color = color
        self.width = width
        self.coords_system.add_content(self)

    def render(self, surface, angle, position):
        self.coords_system.application.render_input.draw_polygon(surface, self.points, position, angle, self.color)

    def set_geometry(self, x1, y1, x2, y2):
        self.points = numpy.array(
            [[x1, y1], [x2 + x1 - 1, y1], [x2 + x1 - 1, y2 + y1 - 1], [x1, y2 + y1 - 1]], float)


class Circle(Shape):
    def __init__(self, coords_system, points: numpy.array, color='red', width=0):
        super().__init__()
        self.coords_system = coords_system
        self.points = points
        self.color = color
        self.width = width
        self.coords_system.add_content(self)

    def render(self, surface, angle, position):
        self.coords_system.application.render_input.draw_circle(surface, self.points, position, angle, self.color)


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

    def render(self, matrix: numpy.array = None, custom_surface=None):
        text_surface = self.render_surface.application.font_storage[self.font_id].render(self.text, True, self.color)
        surface = surface_convertor(self.points, text_surface, matrix, self.render_surface.application)
        # print(matrix)
        if surface[0] is True:
            if custom_surface is not None:
                custom_surface.blit(surface[2], surface[1].tolist())
            else:
                self.render_surface.blit(surface[2], surface[1].tolist())
