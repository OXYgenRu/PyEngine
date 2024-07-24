import numpy
import pygame

import Engine.RenderSurface

import Engine.constants as cs
from Engine.tools import scale_image
import numpy as np


class Camera(Engine.RenderSurface.RenderSurface):
    def __init__(self, display_surface, camera_setting: numpy.array = numpy.array([0, 0, 1, 0.7]), parent_surface=None,
                 render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = numpy.array([0, 0])):
        super().__init__(parent_surface, render_priority, width, height, transfer_vector)
        # camera_setting[0] - x_pos
        # camera_setting[0] - y_pos
        # camera_setting[0] - zoom

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
        x_pos = self.width // 2 - (self.display_surface.width * self.camera_setting[2]) // 2 - (self.camera_setting[
                                                                                                    0] *
                                                                                                self.camera_setting[2])
        y_pos = self.height // 2 - (self.display_surface.height * self.camera_setting[2]) // 2 - (self.camera_setting[
                                                                                                      1] *
                                                                                                  self.camera_setting[
                                                                                                      2])

        self.blit(scale_image(self.application, self.display_surface.rendered_surface, np.array([None, None]),
                              self.camera_setting[2]),
                  (x_pos, y_pos))
        self.rendered_surface = self.copy()

    def camera_motion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.start_pos = event.pos
            self.moving = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.camera_setting[0] += -(event.pos[0] - self.start_pos[0]) / self.camera_setting[2]
            self.camera_setting[1] += -(event.pos[1] - self.start_pos[1]) / self.camera_setting[2]
            self.moving = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.camera_setting[2] = self.camera_setting[2] * self.camera_setting[3]
            else:
                self.camera_setting[2] /= self.camera_setting[3]
        if event.type == pygame.MOUSEMOTION and self.moving is True:
            self.camera_setting[0] += -(event.pos[0] - self.start_pos[0]) / self.camera_setting[2]
            self.camera_setting[1] += -(event.pos[1] - self.start_pos[1]) / self.camera_setting[2]
            self.start_pos = event.pos
