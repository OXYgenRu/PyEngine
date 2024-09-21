import math

import numpy
import numpy as np
import pygame.draw


class RenderInput:
    def __init__(self):
        self.render_scale: float = 1
        self.render_transfer_vector: numpy.array = np.array([0, 0], float)
        self.render_camera_position: numpy.array = np.array([0, 0], float)

    @staticmethod
    def get_rotation_matrix(angle: float) -> numpy.array:
        radians: float = math.radians(angle)
        matrix: np.array = numpy.array(
            [numpy.array([math.cos(radians), -math.sin(radians)]),
             numpy.array([math.sin(radians), math.cos(radians)])], float)
        return matrix

    @staticmethod
    def rotate_vector(vector: numpy.array, angle: float) -> numpy.array:
        return numpy.dot(vector, RenderInput.get_rotation_matrix(angle))

    @staticmethod
    def restore_mesh(points: numpy.array, coords_system_position: numpy.array, angle: float):
        points = points.copy()
        for point_index in range(len(points)):
            points[point_index] = RenderInput.rotate_vector(points[point_index], angle)
            points[point_index] += coords_system_position
        return points

    def set_scale(self, scale: float) -> None:
        self.render_scale = scale

    def set_render_camera_position(self, position: numpy.array) -> None:
        self.render_camera_position = position.copy()

    def set_render_transfer_vector(self, transfer_vector: numpy.array) -> None:
        self.render_transfer_vector = transfer_vector.copy()

    def reset_properties(self):
        self.render_scale = 1
        self.render_transfer_vector = numpy.array([0, 0], float)
        self.render_camera_position: numpy.array = np.array([0, 0], float)

    def transform_mesh(self, points: numpy.array) -> numpy.array:
        for point_index in range(len(points)):
            points[point_index] -= self.render_camera_position - self.render_transfer_vector
            points[point_index] *= self.render_scale
            points[point_index] += self.render_camera_position
        return points

    def draw_polygon(self, surface, points: numpy.array, coords_system_position: numpy.array, angle: float,
                     color: tuple):
        points = points.copy()
        points = self.restore_mesh(points, coords_system_position, angle)
        points = self.transform_mesh(points)
        pygame.draw.polygon(surface, color, points, 0)

    def draw_circle(self, surface, points: numpy.array, coords_system_position: numpy.array, angle: float,
                    color: tuple):
        points = points.copy()
        radius: numpy.array = (points[1][0] - points[0][0]) * self.render_scale
        points = self.restore_mesh(points, coords_system_position, angle)
        points = self.transform_mesh(points)
        pygame.draw.circle(surface, color, points[0], radius)
