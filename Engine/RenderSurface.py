import pygame
import numpy
from collections import defaultdict
from sortedcontainers import SortedSet

import Engine.BasiсShapes


class RenderSurface(pygame.Surface):
    def __init__(self, parent_surface=None, render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = None):
        super().__init__((width, height), pygame.SRCALPHA)

        self.parent_surface = parent_surface
        self.render_priority = render_priority
        self.width = width
        self.height = height
        self.transfer_vector = transfer_vector
        if parent_surface is not None:
            self.application = parent_surface.application
        self.fill_color = (0, 0, 0, 0)

        self.content = []

        self.surfaces = defaultdict(list)
        self.surfaces_priorities = SortedSet()
        if parent_surface is not None:
            parent_surface.surfaces_priorities.add(render_priority)
            parent_surface.surfaces[render_priority].append(self)

    def set_render_priority(self, new_render_priority):
        if len(self.parent_surface.surfaces[self.render_priority]) == 1:
            self.parent_surface.surfaces_priorities.remove(self.render_priority)
        index = self.parent_surface.surfaces[self.render_priority].index(self)
        self.parent_surface.surfaces[self.render_priority].pop(index)
        self.parent_surface.surfaces[new_render_priority].append(self)
        self.render_priority = new_render_priority
        self.parent_surface.surfaces_priorities.add(new_render_priority)

    def add_content(self, content_object):
        self.content.append(content_object)

    def render(self):
        self.fill(self.fill_color)
        for shape in self.content:
            shape.render()
        surfaces_to_bake_list = []
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.render()
                surfaces_to_bake_list.append((surface, tuple(surface.transfer_vector)))
        self.blits(surfaces_to_bake_list)

    def clear_surface(self):
        self.fill(self.fill_color)
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.clear_surface()

    def set_filling(self, color):
        self.fill_color = color

    def add_border(self, color='red'):
        Engine.BasiсShapes.Polygon(self, numpy.array(
            [[0, 0], [self.width - 2, 0], [self.width - 2, self.height - 2], [0, self.height - 2]]), color, 2)
