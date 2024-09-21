import math

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
        self.angle = 0
        self.screen_vector = None

        self.fill_color = (0, 0, 0, 0)
        self.pp = numpy.array([[100, 100], [500, 500], [100, 100]])
        self.content = []
        self.updating_content = []

        self.surfaces = defaultdict(list)
        self.surfaces_priorities = SortedSet()

        self.properties = Engine.PropertyStorage.PropertyStorage()
        self.set_visible_on()

        self.colliders = []
        self.test = 1
        # числа от 0 до 1, для получения координаты умножить на длину и высоту
        self.rotation_pos = numpy.array([0, 0])

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
        if self.test:
            self.fill(self.fill_color)
        for shape in self.content:
            shape.render()
        surfaces_to_bake_list = []
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.render()
                surfaces_to_bake_list.append(
                    (pygame.transform.rotate(surface, surface.angle), tuple(surface.transfer_vector)))
        self.blits(surfaces_to_bake_list)

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

    def update(self, event_list, event_id):
        if self.properties.get(cs.P_UPDATABLE):
            return

        self.on_update(event_list, event_id)
        for element in self.updating_content:
            element.update(event_list, event_id)
        for surface_priority in self.surfaces_priorities:
            for surface in self.surfaces[surface_priority]:
                surface.update(event_list, event_id)

    def on_update(self, args, event_id):
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

    def get_points(self) -> numpy.array:
        rotation_point = numpy.array(
            [self.width * self.rotation_pos[0],
             self.height * self.rotation_pos[1]])
        # print(rotation_point)
        point_1 = numpy.array([self.transfer_vector[0] - rotation_point[0],
                               self.transfer_vector[1] - rotation_point[1]])
        # print(point_1)
        point_2 = numpy.array([self.transfer_vector[0] + (self.width - rotation_point[0]),
                               self.transfer_vector[1] - rotation_point[1]])
        point_3 = numpy.array([self.transfer_vector[0] + (self.width - rotation_point[0]),
                               self.transfer_vector[1] + (self.height - rotation_point[1])])
        point_4 = numpy.array([self.transfer_vector[0] - rotation_point[0],
                               self.transfer_vector[1] + (self.height - rotation_point[1])])
        # print([point_1, point_2, point_3, point_4])
        return numpy.array([point_1, point_2, point_3, point_4])

    def get_vectors(self) -> numpy.array:
        points: numpy.array = self.get_points()
        rotation_point: numpy.array = numpy.array(
            [self.transfer_vector[0], self.transfer_vector[1]])
        vector_1: numpy.array = rotation_point - points[0]
        vector_1 = numpy.array([vector_1[0], vector_1[1], math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2)])
        vector_2: numpy.array = rotation_point - points[1]
        vector_2 = numpy.array([vector_2[0], vector_2[1], math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)])
        vector_3: numpy.array = rotation_point - points[2]
        vector_3 = numpy.array([vector_3[0], vector_3[1], math.sqrt(vector_3[0] ** 2 + vector_3[1] ** 2)])
        vector_4: numpy.array = rotation_point - points[3]
        vector_4 = numpy.array([vector_4[0], vector_4[1], math.sqrt(vector_4[0] ** 2 + vector_4[1] ** 2)])
        # print([vector_1, vector_2, vector_3, vector_4])
        return numpy.array([vector_1, vector_2, vector_3, vector_4])

    def get_surface(self) -> tuple:
        rotated_surface: pygame.surface.Surface = pygame.transform.rotate(self, self.angle)
        vectors: numpy.array = self.get_vectors()

        angle_1: float = math.atan2(vectors[0][1], vectors[0][0]) - math.radians(self.angle)

        vector_1: numpy.array = numpy.array([vectors[0][2] * math.cos(angle_1), vectors[0][2] * math.sin(angle_1)])

        angle_2: float = math.atan2(vectors[1][1], vectors[1][0]) - math.radians(self.angle)
        vector_2: numpy.array = numpy.array([vectors[1][2] * math.cos(angle_2), vectors[1][2] * math.sin(angle_2)])

        angle_3: float = math.atan2(vectors[2][1], vectors[2][0]) - math.radians(self.angle)
        vector_3: numpy.array = numpy.array([vectors[2][2] * math.cos(angle_3), vectors[2][2] * math.sin(angle_3)])

        angle_4: float = math.atan2(vectors[3][1], vectors[3][0]) - math.radians(self.angle)
        vector_4: numpy.array = numpy.array([vectors[3][2] * math.cos(angle_4), vectors[3][2] * math.sin(angle_4)])
        # print(math.degrees(math.atan2(vectors[3][1], vectors[3][0])))
        shift_x = -max(vector_1.tolist()[0], vector_2.tolist()[0], vector_3.tolist()[0], vector_4.tolist()[0])
        shift_y = min(-vector_1.tolist()[1], -vector_2.tolist()[1], -vector_3.tolist()[1], -vector_4.tolist()[1])
        return numpy.array([shift_x, shift_y]), rotated_surface
