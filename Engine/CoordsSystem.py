import random

import numpy
import pygame
import numpy as np

import Engine.BasiсObjects
from Engine.PropertyStorage import PropertyStorage
from collections import defaultdict
from sortedcontainers import SortedSet
import Engine.constants as cs
from Engine.RenderSystem.RenderInput import RenderInput


class CoordsSystem:
    def __init__(self, parent=None, render_priority: int = 0, position: np = np.array([0, 0], float), angle: float = 0):
        self.parent = parent
        self.render_priority: int = render_priority
        self.position: np.array = position
        # self.render_transfer_vector: np.array = np.array([0, 0])
        # self.render_scale: float = 1
        self.angle: float = angle
        self.content: list = []
        self.ui_colliders: list = []
        self.properties: PropertyStorage = PropertyStorage()
        # self.rotation_position: np.array = np.array([0, 0])
        self.connected_coords_systems: defaultdict = defaultdict(list)
        self.connected_coords_systems_priorities: SortedSet = SortedSet()
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        if parent is not None:
            self.application = parent.application
            parent.connected_coords_systems_priorities.add(render_priority)
            parent.connected_coords_systems[render_priority].append(self)

        self.y_direction = Engine.BasiсObjects.Polygon(self, numpy.array([[-1, 0], [-1, 50], [1, 50], [1, 0]], float),
                                                       'red')
        self.x_direction = Engine.BasiсObjects.Polygon(self, numpy.array([[0, -1], [50, -1], [50, 1], [0, 1]], float),
                                                       'blue')

    def add_content(self, new_content):
        self.content.append(new_content)

    def set_visible_on(self) -> None:
        self.properties.update(cs.P_VISIBLE, False)

    def set_visible_off(self) -> None:
        self.properties.update(cs.P_VISIBLE, True)

    def set_updatable_on(self) -> None:
        self.properties.update(cs.P_UPDATABLE, False)

    def set_updatable_off(self) -> None:
        self.properties.update(cs.P_UPDATABLE, True)

    def set_ui_colliders_disable(self) -> None:
        self.properties.update(cs.P_UI_COLLIDERS, True)

    def set_ui_colliders_enable(self) -> None:
        self.properties.update(cs.P_UI_COLLIDERS, False)

    def add_coords_system(self, new_system):
        self.connected_coords_systems_priorities.add(new_system.render_priority)
        self.connected_coords_systems[new_system.render_priority].append(new_system)

    def render(self, surface, position: numpy.array = np.array([0, 0]), angle: float = 0):
        if self.properties.get(cs.P_VISIBLE):
            return
        rotation_matrix: np.array = self.application.render_input.get_rotation_matrix(
            angle)
        for content in self.content:
            content.render(surface, angle, position)
        for system_priority in self.connected_coords_systems_priorities:
            for coords_system in self.connected_coords_systems[system_priority]:
                new_angle: float = angle + coords_system.angle
                new_vector = np.dot(coords_system.position, rotation_matrix)
                coords_system.render(surface, position + new_vector, new_angle)

    def update(self, event_list, event_id):
        if self.properties.get(cs.P_UPDATABLE):
            return
        self.on_update(event_list, event_id)
        # for element in self.content:
        #     element.update(event_list, event_id)
        for system_priority in self.connected_coords_systems_priorities:
            for coords_system in self.connected_coords_systems[system_priority]:
                coords_system.update(event_list, event_id)

    def on_update(self, event_list, event_id):
        pass
