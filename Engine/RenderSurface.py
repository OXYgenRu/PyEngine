import numpy as np
import pygame
import numpy
from collections import defaultdict
from sortedcontainers import SortedSet

import Engine.BasiсObjects
import Engine.PropertyStorage
import Engine.constants as cs


class RenderSurface(pygame.Surface):
    def __init__(self, parent_surface=None, render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = numpy.array([0, 0])):
        super().__init__((width, height), pygame.SRCALPHA)

        self.border = None
        self.parent_surface = parent_surface
        self.render_priority = render_priority
        self.width = width
        self.height = height
        self.border_surface = None
        self.rendered_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rendered_surface.fill((0, 0, 0, 0))
        self.transfer_vector = transfer_vector
        self.screen_vector = None

        self.fill_color = (0, 0, 0, 0)

        self.content = []
        self.updating_content = []

        self.surfaces = defaultdict(list)
        self.surfaces_priorities = SortedSet()

        self.properties = Engine.PropertyStorage.PropertyStorage()
        self.set_visible_on()

        self.colliders = []

        if parent_surface is not None:
            self.application = parent_surface.application
            parent_surface.surfaces_priorities.add(render_priority)
            parent_surface.surfaces[render_priority].append(self)
            self.screen_vector = self.transfer_vector + parent_surface.transfer_vector

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
        self.updating_content.append(content_object)

    def add_updating_content(self, content_object):
        self.updating_content.append(content_object)

    def render(self):
        if self.properties.get(cs.P_HIDED):
            return
        for shape in self.content:
            shape.render()
        surfaces_to_bake_list = []
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.render()
                surfaces_to_bake_list.append((surface, tuple(surface.transfer_vector)))
        self.blits(surfaces_to_bake_list)

    def clear_surface(self):
        if self.properties.get(cs.P_HIDED):
            return
        self.fill(self.fill_color)
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.clear_surface()

    def set_filling(self, color):
        self.fill_color = color

    def add_border(self, color='red'):

        self.border = Engine.BasiсObjects.Polygon(self, numpy.array(
            [[0, 0], [self.width - 2, 0], [self.width - 2, self.height - 2], [0, self.height - 2]]), color, 2)

    def hide_border(self):
        self.border_surface.set_visible_off()

    def show_border(self):
        self.border_surface.set_visible_on()

    def set_visible_off(self):
        self.properties.update(cs.P_HIDED, True)

    def set_visible_on(self):
        self.properties.update(cs.P_HIDED, False)

    def set_updatable_off(self):
        self.properties.update(cs.P_UPDATABLE, True)

    def set_updatable_on(self):
        self.properties.update(cs.P_UPDATABLE, False)

    def disable_ui_colliders(self):
        self.properties.update(cs.P_UI_COLLIDERS, True)

    def enable_ui_colliders(self):
        self.properties.update(cs.P_UI_COLLIDERS, False)

    def update(self, args):
        if self.properties.get(cs.P_UPDATABLE):
            return

        self.on_update(args)
        for element in self.updating_content:
            element.update(args)
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.update(args)

    def on_update(self, args):
        pass

    def move(self, transfer_vector: np.array):
        self.transfer_vector += transfer_vector

    def set_point(self, point: np.array):
        new_vector = point - self.transfer_vector
        self.move(new_vector)

    def update_ui_colliders(self, mouse_event: pygame.event.Event, mouse_pos: numpy.array):
        if self.properties.get(cs.P_UI_COLLIDERS):
            return
        reversed_list = list(self.surfaces_priorities)[::-1]
        flag = False
        for surface_priority in reversed_list:
            for surface in self.surfaces[surface_priority]:
                flag = surface.update_ui_colliders(mouse_event, mouse_pos - surface.transfer_vector)
                if flag is True:
                    return True
        for ui_collider in self.colliders:
            flag = ui_collider.mouse_event_update(mouse_event, mouse_pos)
            if flag is True:
                return True
        return False
    # def get_points(self):
    #     numpy
