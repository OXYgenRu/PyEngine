import numpy
import numpy as np
import pygame
from PIL import Image
from PIL import Image, ImageGrab, ImageOps
import Engine.constants as cs
import cv2
import cupy as cp


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
