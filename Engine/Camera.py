import numpy
import pygame

import Engine.RenderSurface

import Engine.constants as cs
from Engine.tools import scale_image
import numpy as np


class Camera(Engine.RenderSurface.RenderSurface):
    def __init__(self, display_surface, camera_setting: numpy.array = numpy.array([0, 0, 1, 0.7]), parent_surface=None,
                 render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = numpy.array([0, 0]), zoom_restrictions: numpy.array = None):
        super().__init__(parent_surface, render_priority, width, height, transfer_vector)
        # camera_setting[0] - x_pos
        # camera_setting[0] - y_pos
        # camera_setting[0] - zoom

        self.on_surface_rect = None
        self.zoom_restrictions = zoom_restrictions
        self.on_surface_pos = numpy.array([0, 0, 0, 0], dtype=float)
        self.height_ = height
        self.width_ = width
        self.new_y_pos_ = 0
        self.on_surface_camera_x_pos = 0
        self.moving = False
        self.start_pos = None
        self.display_surface = display_surface
        self.camera_setting = camera_setting

    def render(self):
        if self.properties.get(cs.P_HIDED):
            return
        self.fill(self.fill_color)
        for shape in self.content:
            shape.render()
        self.on_surface_pos = numpy.array([0, 0, 0, 0], dtype=float)
        self.on_surface_pos[0] = self.display_surface.width // 2 - self.width * self.camera_setting[2] // 2
        self.on_surface_pos[0] -= self.camera_setting[0]
        self.on_surface_pos[1] = self.display_surface.height // 2 - self.height * self.camera_setting[2] // 2
        self.on_surface_pos[1] -= self.camera_setting[1]

        self.on_surface_pos[2] = self.width * self.camera_setting[2] + self.on_surface_pos[0]
        self.on_surface_pos[3] = self.height * self.camera_setting[2] + self.on_surface_pos[1]

        self.on_surface_rect = numpy.array([0, 0, 0, 0, 0, 0], dtype=float)
        self.on_surface_rect[0] = max(0, float(self.on_surface_pos[0]))
        self.on_surface_rect[0] = min(self.display_surface.width, float(self.on_surface_rect[0]))
        self.on_surface_rect[1] = max(0, float(self.on_surface_pos[1]))
        self.on_surface_rect[1] = min(self.display_surface.height, float(self.on_surface_rect[1]))
        self.on_surface_rect[2] = max(0, float(self.on_surface_pos[2]))
        self.on_surface_rect[2] = min(self.display_surface.width, int(self.on_surface_rect[2]))
        self.on_surface_rect[3] = max(0, float(self.on_surface_pos[3]))
        self.on_surface_rect[3] = min(self.display_surface.height, float(self.on_surface_rect[3]))

        self.on_surface_rect[4] = self.on_surface_rect[2] - self.on_surface_rect[0]
        self.on_surface_rect[5] = self.on_surface_rect[3] - self.on_surface_rect[1]
        self.on_surface_rect[4] = min(self.display_surface.width - self.on_surface_rect[0],
                                      float(self.on_surface_rect[4] + 10))
        self.on_surface_rect[5] = min(self.display_surface.height - self.on_surface_rect[1],
                                      float(self.on_surface_rect[5] + 10))

        img = self.display_surface.rendered_surface.subsurface(self.on_surface_rect[0], self.on_surface_rect[1],
                                                               self.on_surface_rect[4],
                                                               self.on_surface_rect[5])
        img = scale_image(self.application, img, np.array([None, None]),
                          1 / self.camera_setting[2])
        x_pos = (self.on_surface_rect[0] - self.on_surface_pos[0] - self.on_surface_pos[0] % 1) / self.camera_setting[2]
        y_pos = (self.on_surface_rect[1] - self.on_surface_pos[1] - self.on_surface_pos[1] % 1) / self.camera_setting[2]
        self.blit(img, (x_pos, y_pos))
        self.rendered_surface = self.copy()

    def on_update(self, args):
        if cs.E_EVENT in args:
            event = args[cs.E_EVENT]
            self.camera_motion(event)

    def camera_motion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.start_pos = event.pos
            self.moving = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.camera_setting[0] += (event.pos[0] - self.start_pos[0]) * self.camera_setting[2]
            self.camera_setting[1] += (event.pos[1] - self.start_pos[1]) * self.camera_setting[2]
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
            self.camera_setting[0] += (event.pos[0] - self.start_pos[0]) * self.camera_setting[2]
            self.camera_setting[1] += (event.pos[1] - self.start_pos[1]) * self.camera_setting[2]
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
