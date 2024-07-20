import numpy as np
import pygame

from Engine.tools import scale_image


class Animation:
    def __init__(self, image, frames_cnt, fps, animation_id):
        self.image = image
        self.frames_cnt = frames_cnt
        self.fps = fps
        self.animation_id = animation_id
        self.frames = []
        self.cut_frames()

    def cut_frames(self):
        width = self.image.get_width() // self.frames_cnt
        height = self.image.get_height()
        for i in range(self.frames_cnt):
            frame_location = (width * i, 0)
            self.frames.append(self.image.subsurface(pygame.Rect(frame_location, (width, height))))

    def get_frames(self):
        return self.frames
