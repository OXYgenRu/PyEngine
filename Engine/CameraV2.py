import numpy
import pygame

import Engine.RenderSurface

import Engine.constants as cs
from Engine.tools import scale_image, render_surface_convertor
import numpy as np


class Camera(Engine.RenderSurface.RenderSurface):
    def __init__(self, connected_surface, camera_setting: numpy.array = numpy.array([0, 0, 1, 0.7]),
                 parent_surface=None,
                 render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = numpy.array([0, 0]), zoom_restrictions: numpy.array = None):
        super().__init__(parent_surface, render_priority, width, height, transfer_vector)
        # camera_setting[0] - x_pos
        # camera_setting[0] - y_pos
        # camera_setting[0] - zoom

        self.on_surface_rect = None
        self.zoom_restrictions = zoom_restrictions
        self.connected_surface = connected_surface
        self.on_surface_pos = numpy.array([0, 0, 0, 0], dtype=float)
        self.new_y_pos_ = 0
        self.on_surface_camera_x_pos = 0
        self.moving = False
        self.start_pos = None
        self.camera_setting = camera_setting.copy()
        self.connected_surface.set_visible_off()
        self.connected_surface.disable_ui_colliders()

    def render(self):
        if self.properties.get(cs.P_HIDED):
            return
        matrix = [0, 0, self.width * self.camera_setting[2], self.width, self.height * self.camera_setting[2],
                  self.height, self.camera_setting[0] * self.camera_setting[2],
                  self.camera_setting[1] * self.camera_setting[2], self.camera_setting[2]]
        for shape in self.connected_surface.content:
            shape.render(numpy.array(matrix), self)
        surfaces_to_bake_list = []
        for surface_priority in self.connected_surface.surfaces_priorities:
            for surface in self.connected_surface.surfaces[surface_priority]:
                surface.render()
                current_surface = render_surface_convertor(surface, matrix)
                surfaces_to_bake_list.append((current_surface[1], current_surface[0]))
        self.blits(surfaces_to_bake_list)

    def clear_surface(self):
        self.fill(self.fill_color)
        for surface_priority in self.connected_surface.surfaces_priorities:
            for surface in self.connected_surface.surfaces[surface_priority]:
                surface.clear_surface()

    def on_update(self, args):
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            self.camera_motion(event)

    def camera_motion(self, event):
        if self.properties.get("locked"):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.start_pos = event.pos
            self.moving = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.camera_setting[0] += (event.pos[0] - self.start_pos[0]) / self.camera_setting[2]
            self.camera_setting[1] += (event.pos[1] - self.start_pos[1]) / self.camera_setting[2]
            self.moving = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.camera_setting[2] = self.camera_setting[2] * self.camera_setting[3]
            else:
                self.camera_setting[2] /= self.camera_setting[3]
            if self.zoom_restrictions is not None:
                self.camera_setting[2] = max(self.camera_setting[2], self.zoom_restrictions[1])
                self.camera_setting[2] = min(self.camera_setting[2], self.zoom_restrictions[0])
        if event.type == pygame.MOUSEMOTION and self.moving is True:
            self.camera_setting[0] += (event.pos[0] - self.start_pos[0]) / self.camera_setting[2]
            self.camera_setting[1] += (event.pos[1] - self.start_pos[1]) / self.camera_setting[2]
            self.start_pos = event.pos

    def set_settings(self, x_pos=None, y_pos=None, zoom=None, zoom_sensitivity=None):
        if x_pos is not None:
            self.camera_setting[0] = x_pos
        if y_pos is not None:
            self.camera_setting[1] = y_pos
        if zoom is not None:
            self.camera_setting[2] = zoom
        if zoom_sensitivity is not None:
            self.camera_setting[3] = zoom_sensitivity

    def set_lock(self):
        self.properties.update("locked", True)

    def set_unlock(self):
        self.properties.update("locked", False)

    def update_ui_colliders(self, mouse_event: pygame.event.Event, mouse_pos):
        reversed_list = list(self.connected_surface.surfaces_priorities)[::-1]
        flag = False
        vector = -numpy.array(
            [self.width // 2, self.height // 2], dtype=float) + numpy.array([mouse_pos[0], mouse_pos[1]], dtype=float)
        vector /= self.camera_setting[2]
        vector -= numpy.array(
            [self.camera_setting[0], self.camera_setting[1]], dtype=float)
        vector += numpy.array(
            [self.width // 2, self.height // 2])
        # print(vector)
        for surface_priority in reversed_list:
            for surface in self.connected_surface.surfaces[surface_priority]:
                flag = surface.update_ui_colliders(mouse_event, vector.tolist())
                if flag is True:
                    return True
        for ui_collider in self.connected_surface.colliders:
            flag = ui_collider.mouse_event_update(mouse_event, vector.tolist())
            if flag is True:
                return True
        return False
