import numpy
import numpy as np
import pygame
import shapely
from PIL import Image
from PIL import Image, ImageGrab, ImageOps
import Engine.constants as cs


def scale_image(application, pygame_image, new_size: numpy.array = None, scale=None):
    if scale == 1:
        return pygame_image
    if scale is not None:
        new_size = (int(pygame_image.get_rect().width * scale), int(pygame_image.get_rect().height * scale))
    elif new_size[0] is not None and new_size[1] is not None:
        new_size = (int(new_size[0]), int(new_size[1]))
    elif new_size[0] is not None and new_size[1] is None:
        scale_cnt = new_size[0] / pygame_image.get_rect().width
        new_size = (int(pygame_image.get_rect().width * scale_cnt), int(pygame_image.get_rect().height * scale_cnt))
    elif new_size[0] is None and new_size[1] is not None:
        scale_cnt = new_size[1] / pygame_image.get_rect().width
        new_size = (int(pygame_image.get_rect().width * scale_cnt), int(pygame_image.get_rect().height * scale_cnt))

    if application.get_property(cs.P_SCALING_TYPE) == cs.P_SCALING_TYPE_PILLOW:
        pygame_image_str = pygame.image.tostring(pygame_image, 'RGBA')
        pillow_image = Image.frombytes('RGBA', pygame_image.get_size(), pygame_image_str)
        scaled_pillow_image = pillow_image.resize(new_size)
        pygame_image_scaled = pygame.image.fromstring(scaled_pillow_image.tobytes(), scaled_pillow_image.size,
                                                      'RGBA')
        return pygame_image_scaled
    elif application.get_property(cs.P_SCALING_TYPE) == cs.P_SCALING_TYPE_PYGAME:
        scaled_image = pygame.transform.scale(pygame_image, new_size)
        return scaled_image
    elif application.get_property(cs.P_SCALING_TYPE) == cs.P_SCALING_TYPE_HYBRID:
        new_square = new_size[0] * new_size[1]
        square = pygame_image.get_rect().width * pygame_image.get_rect().height
        # print(square, new_square)
        if square > new_square:
            pygame_image_str = pygame.image.tostring(pygame_image, 'RGBA')
            pillow_image = Image.frombytes('RGBA', pygame_image.get_size(), pygame_image_str)
            scaled_pillow_image = pillow_image.resize(new_size)
            pygame_image_scaled = pygame.image.fromstring(scaled_pillow_image.tobytes(), scaled_pillow_image.size,
                                                          'RGBA')
            return pygame_image_scaled
        else:
            # print(1)
            scaled_image = pygame.transform.scale(pygame_image, new_size)
            return scaled_image


def surface_convertor(point, surface, matrix: numpy.array = None, application=None):
    if matrix is not None:
        point1 = point
        width = surface.get_rect().width
        height = surface.get_rect().height
        point2 = point1 + numpy.array([width, 0])
        point3 = point1 + numpy.array([width, height])
        point4 = point1 + numpy.array([0, height])
        polygon = numpy.array([point1, point2, point3, point4])
        new_polygon = polygon_converter(polygon, matrix)
        new_size = new_polygon[2] - new_polygon[0]
        return True, new_polygon[0], scale_image(application, surface, new_size, None)

    else:
        return True, point, surface


def rect_intersection(surface_polygon: numpy.array, camera_polygon: numpy.array):
    x_left = max(surface_polygon[0][0], camera_polygon[0][0])
    y_top = max(surface_polygon[0][1], camera_polygon[0][1])
    x_right = min(surface_polygon[1][0], camera_polygon[1][0])
    y_bottom = min(surface_polygon[2][1], camera_polygon[2][1])
    if x_left < x_right and y_top < y_bottom:
        return True, numpy.array([[x_left, y_top], [x_right, y_top], [x_right, y_bottom], [x_left, y_bottom]])
    else:
        return False, numpy.array([])


def render_surface_convertor(surface, matrix: numpy.array = None) -> tuple:
    if matrix is not None:
        point1 = numpy.array([surface.transfer_vector[0] - surface.width * surface, surface.transfer_vector[1]])
        point2 = point1 + numpy.array([surface.width, 0])
        point3 = point1 + numpy.array([surface.width, surface.height])
        point4 = point1 + numpy.array([0, surface.height])
        polygon = numpy.array([point1, point2, point3, point4])
        new_polygon = polygon_converter(polygon, matrix)

        points_list = [tuple(point) for point in new_polygon]
        shapely_polygon = shapely.Polygon(points_list)

        camera_polygon = shapely.Polygon([(0, 0), (matrix[3], 0), (matrix[3], matrix[5]), (0, matrix[5])])
        to_show_polygon = shapely_polygon.intersection(camera_polygon)
        new_size = new_polygon[2] - new_polygon[0]
        return new_polygon[0], scale_image(surface.application, surface, new_size, None)
    else:
        return surface.transfer_vector, surface


def polygon_converter(points, matrix=None) -> numpy.array:
    camera_matrix = numpy.array(
        [[1, 0], [0, 1], [-0.5, 0], [0.5, 0], [0, -0.5], [0, 0.5], [1, 0], [0, 1], [0, 0]], dtype=float)
    if matrix is not None:
        new_points = numpy.empty(len(points), object)
        for i in range(len(points)):
            new_points[i] = []
            matrix[0] = points[i][0] * matrix[8]
            matrix[1] = points[i][1] * matrix[8]
            new_points[i] = numpy.dot(matrix, camera_matrix)

        return new_points
    else:
        return points

# def rotate_render_surface(point,render_surface, angle):
