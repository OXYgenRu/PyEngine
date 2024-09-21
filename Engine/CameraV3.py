import numpy
import pygame

from Engine.CoordsSystem import CoordsSystem
import numpy as np
import Engine.constants as cs
from Engine.RenderSystem.RenderInput import RenderInput


class Camera(CoordsSystem):
    def __init__(self, parent=None, render_priority: int = 0, position: np = np.array([0, 0], float), angle: float = 0,
                 target=None):
        super().__init__(parent, render_priority, position, angle)
        self.render_transfer_vector: np.array = np.array([0, 0], float)
        self.scale: float = 1
        self.camera_angle: float = 0
        self.target = target
        self.moving = False
        self.start_pos = None
        self.zoom_sensitivity = 0.75
        self.content = target.content
        self.connected_coords_systems_priorities = target.connected_coords_systems_priorities
        self.connected_coords_systems = target.connected_coords_systems

    def on_update(self, events_list, event_id):
        self.camera_motion(events_list)

    def camera_motion(self, events_list):
        for event in events_list:
            if event[0] == cs.E_EVENT:
                if event[1].type == pygame.MOUSEBUTTONDOWN and event[1].button == 2:
                    self.start_pos = event[1].pos
                    self.moving = True
                if event[1].type == pygame.MOUSEBUTTONUP and event[1].button == 2:
                    self.render_transfer_vector[0] += (event[1].pos[0] - self.start_pos[0]) / self.scale
                    self.render_transfer_vector[1] += (event[1].pos[1] - self.start_pos[1]) / self.scale
                    # print(vector)
                    self.moving = False
                if event[1].type == pygame.MOUSEWHEEL:
                    if event[1].y > 0:
                        self.scale = self.scale * self.zoom_sensitivity
                    else:
                        self.scale /= self.zoom_sensitivity
                if event[1].type == pygame.MOUSEMOTION and self.moving is True:
                    self.render_transfer_vector[0] += (event[1].pos[0] - self.start_pos[0]) / self.scale
                    self.render_transfer_vector[1] += (event[1].pos[1] - self.start_pos[1]) / self.scale
                    self.start_pos = event[1].pos

    def render(self, surface, position: numpy.array = np.array([0, 0]), angle: float = 0):
        if self.properties.get(cs.P_VISIBLE):
            return
        self.application.render_input.set_scale(self.scale)
        self.application.render_input.set_render_transfer_vector(self.render_transfer_vector)
        self.application.render_input.set_render_camera_position(position)
        rotation_matrix: np.array = self.application.render_input.get_rotation_matrix(
            angle + self.camera_angle)
        for content in self.content:
            content.render(surface, angle + self.camera_angle, position)
        for system_priority in self.connected_coords_systems_priorities:
            for coords_system in self.connected_coords_systems[system_priority]:
                new_angle: float = angle + coords_system.angle + self.camera_angle
                new_vector = np.dot(coords_system.position, rotation_matrix)
                coords_system.render(surface, position + new_vector, new_angle)
        self.application.render_input.reset_properties()
