from collections import defaultdict

import pygame

from Engine.Animations.Animation import Animation
import numpy as np
from Engine.tools import scale_image
import Engine.constants as cs


class Animator:
    def __init__(self, application, default_animation, size: np.array = np.array([None, None]), scale=None):
        self.application = application
        self.animations = defaultdict(None)
        default_animation = Animator.init_default_animation(default_animation)
        self.animations[default_animation.animation_id] = default_animation
        self.active_animation_id = default_animation.animation_id

        self.default_animation = default_animation
        self.original_frames = []
        self.current_frame_id = 0
        self.frames_cnt = 0
        self.fps = 0
        self.size = size
        self.scale = scale
        self.event_number = -1
        self.stop_animation_event = 0
        self.playing_cnt = -1
        self.angle = 0
        self.symmetrically_x = False
        self.symmetrically_y = False

        self.load_animation(self.active_animation_id)

    @staticmethod
    def init_default_animation(default_animation):
        if default_animation is None:
            surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))
            return Animation(surface, 1, 1, "default")
        if type(default_animation) is not pygame.surface.Surface:
            return default_animation
        else:
            return Animation(default_animation, 1, 1, "default")

    def get_frame(self):
        frame = self.original_frames[self.current_frame_id]
        self.current_frame_id = (self.current_frame_id + 1) % self.frames_cnt
        if self.current_frame_id == 0 and self.playing_cnt >= 1:
            self.playing_cnt -= 1
        if self.playing_cnt == 0:
            self.playing_cnt = -1
            self.load_default_animation()
        return self.adapt_frame(frame)
        # return scale_image(self.application, frame, self.size, self.scale)

    def adapt_frame(self, frame):
        frame = scale_image(self.application, frame, self.size, self.scale)
        frame = pygame.transform.flip(frame, self.symmetrically_x, self.symmetrically_y)
        frame = pygame.transform.rotate(frame, self.angle)
        return frame

    def get_current_frame(self):
        return self.adapt_frame(self.original_frames[self.current_frame_id])
        # return scale_image(self.application, self.original_frames[self.current_frame_id], self.size, self.scale)

    def get_active_animation(self) -> Animation:
        return self.animations[self.active_animation_id]

    def get_animation(self, animation_id) -> Animation:
        return self.animations[animation_id]

    def resize(self, size: np.array = np.array([None, None]), scale=None):
        self.scale = scale
        self.size = size

    def load_animation(self, animation_id, playing_time=None, playing_cnt=None):
        animation = self.get_animation(animation_id)
        self.angle = 0
        self.symmetrically_x = False
        self.symmetrically_y = False
        self.original_frames = animation.frames
        self.frames_cnt = animation.frames_cnt
        self.active_animation_id = animation.animation_id
        self.fps = animation.fps
        self.current_frame_id = 0
        self.resize(self.size, self.scale)
        if self.event_number != -1:
            self.application.delete_timer(self.event_number)
        self.event_number = self.application.set_timer(int(1000 / self.fps))
        if playing_time is not None:
            self.stop_animation_event = self.application.set_timer(playing_time)
        if playing_cnt is not None:
            self.playing_cnt = playing_cnt
        pygame.event.post(pygame.event.Event(cs.E_START_NEW_ANIMATION))

    def load_default_animation(self):
        self.load_animation(self.default_animation.animation_id)

    def add_animation(self, animation):
        self.animations[animation.animation_id] = animation

    def update(self, args):
        if cs.E_EVENT in args:
            if args[cs.E_EVENT].type == pygame.USEREVENT + self.stop_animation_event:
                self.application.delete_timer(self.stop_animation_event)
                self.load_default_animation()
