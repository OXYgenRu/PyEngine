import math

import numpy
import pygame
import shapely

import Engine.RenderSurface

import Engine.constants as cs
from Engine.tools import scale_image, render_surface_convertor, surface_convertor, rect_intersection, polygon_converter
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
        self.camera_polygon = []

    def render(self):
        if self.properties.get(cs.P_HIDED):
            return
        self.fill(self.fill_color)
        width = self.width / self.camera_setting[2] / 2
        height = self.height / self.camera_setting[2] / 2
        self.camera_polygon = numpy.array(
            [[-self.camera_setting[0] + self.width // 2 - width - 10,
              -self.camera_setting[1] + self.height // 2 - height - 10],
             [-self.camera_setting[0] + self.width // 2 + width + 10,
              -self.camera_setting[1] + self.height // 2 - height - 10],
             [-self.camera_setting[0] + self.width // 2 + width + 10,
              -self.camera_setting[1] + self.height // 2 + height + 10],
             [-self.camera_setting[0] + self.width // 2 - width - 10,
              -self.camera_setting[1] + self.height // 2 + height + 10]])
        matrix = [0, 0, self.width * self.camera_setting[2], self.width, self.height * self.camera_setting[2],
                  self.height, self.camera_setting[0] * self.camera_setting[2],
                  self.camera_setting[1] * self.camera_setting[2], self.camera_setting[2]]
        for shape in self.connected_surface.content:
            shape.render(numpy.array(matrix), self)
        surfaces_to_bake_list = []
        for surface_priority in self.connected_surface.surfaces_priorities:
            for surface in self.connected_surface.surfaces[surface_priority]:
                if self.inter(surface.transfer_vector, surface):
                    surface.render()
                    cnt += 1
                    rotated_surface = surface.get_surface()
                    current_surface = self.surface_culling(surface.transfer_vector + rotated_surface[0],
                                                           rotated_surface[1],
                                                           matrix)
                    if current_surface[0] is True:
                        surfaces_to_bake_list.append(
                            (current_surface[2], (current_surface[1][0],
                                                  current_surface[1][1])))
        # print(cnt)
        self.blits(surfaces_to_bake_list)

    def on_update(self, events_list, event_id):
        self.camera_motion(events_list)

    def camera_motion(self, events_list):
        if self.properties.get("locked"):
            return
        for event in events_list:
            if event[0] == cs.E_EVENT:
                if event[1].type == pygame.MOUSEBUTTONDOWN and event[1].button == 2:
                    self.start_pos = event[1].pos
                    self.moving = True
                if event[1].type == pygame.MOUSEBUTTONUP and event[1].button == 2:
                    self.camera_setting[0] += (event[1].pos[0] - self.start_pos[0]) / self.camera_setting[2]
                    self.camera_setting[1] += (event[1].pos[1] - self.start_pos[1]) / self.camera_setting[2]
                    self.moving = False
                if event[1].type == pygame.MOUSEWHEEL:
                    if event[1].y > 0:
                        self.camera_setting[2] = self.camera_setting[2] * self.camera_setting[3]
                    else:
                        self.camera_setting[2] /= self.camera_setting[3]
                    if self.zoom_restrictions is not None:
                        self.camera_setting[2] = max(self.camera_setting[2], self.zoom_restrictions[1])
                        self.camera_setting[2] = min(self.camera_setting[2], self.zoom_restrictions[0])
                if event[1].type == pygame.MOUSEMOTION and self.moving is True:
                    self.camera_setting[0] += (event[1].pos[0] - self.start_pos[0]) / self.camera_setting[2]
                    self.camera_setting[1] += (event[1].pos[1] - self.start_pos[1]) / self.camera_setting[2]
                    self.start_pos = event[1].pos

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

    def surface_culling(self, point, surface, matrix) -> list:
        if matrix is not None:
            surface_rect: pygame.Rect = surface.get_rect()
            surface_polygon: numpy.array = numpy.array([point, [point[0] + surface_rect.width, point[1]],
                                                        [point[0] + surface_rect.width, point[1] + surface_rect.height],
                                                        [point[0], point[1] + surface_rect.height]])
            intersection = rect_intersection(surface_polygon, self.camera_polygon)
            if not intersection[0]:
                return [False]
            subsurface_polygon = intersection[1] - surface_polygon[0]
            listed_subsurface_polygon = subsurface_polygon.tolist()

            sub_surface_rect = pygame.Rect(listed_subsurface_polygon[0][0], listed_subsurface_polygon[0][1],
                                           math.floor(
                                               listed_subsurface_polygon[1][0] - listed_subsurface_polygon[0][0]),
                                           math.floor(
                                               listed_subsurface_polygon[2][1] - listed_subsurface_polygon[1][1]))

            sub_surface = None
            vector = numpy.array([sub_surface_rect.x + point[0], point[1] + sub_surface_rect.y])
            new_vector = polygon_converter(numpy.array([vector]), matrix)

            if np.array_equal(intersection[1], surface_polygon):
                sub_surface = surface
            else:
                sub_surface = surface.subsurface(sub_surface_rect)
            size = numpy.array([[0, 0], [sub_surface_rect.w, sub_surface_rect.h]])
            ss = polygon_converter(size, matrix)
            new_size = ss[1] - ss[0] + 1

            finish_surface = scale_image(self.application, sub_surface,
                                         np.ceil(new_size),
                                         None)
            return [True,
                    new_vector[0],
                    finish_surface]
        else:
            return [True, point, surface]

    def inter(self, point, surface):
        surface_rect: pygame.Rect = surface.get_rect()
        surface_polygon: numpy.array = numpy.array([point, [point[0] + surface_rect.width, point[1]],
                                                    [point[0] + surface_rect.width, point[1] + surface_rect.height],
                                                    [point[0], point[1] + surface_rect.height]])
        intersection = rect_intersection(surface_polygon, self.camera_polygon)
        if not intersection[0]:
            return False
        else:
            return True
