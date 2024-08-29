from collections import defaultdict

import pygame

from Engine.Animations.Animation import Animation
import numpy as np
from Engine.tools import scale_image
import Engine.constants as cs
import Engine.StateMachine.StateMachine


class Animator:
    def __init__(self, application, default_animation, size: np.array = np.array([None, None]), scale=None):
        self.application = application
        self.animations = defaultdict(None)
        default_animation = Animator.init_default_animation(default_animation)
        self.animations[default_animation.animation_id] = default_animation
        self.active_animation_id = default_animation.animation_id

        self.default_animation = default_animation
        self.original_frames = []
        self.frames = []
        self.adapted_frame = []
        self.current_frame_id = 0
        self.frames_cnt = 0
        self.fps = 0
        self.size = size
        self.scale = scale
        self.event_number = -1
        self.stop_animation_event = -1
        self.playing_cnt = -1
        self.angle = 0
        self.end_of_animation = False
        self.symmetrically_x = False
        self.symmetrically_y = False
        self.connected_state_machine = None
        self.updated = False

        self.load_animation(self.active_animation_id)

    @staticmethod
    def init_default_animation(default_animation):
        if default_animation is None:
            surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))
            return Animation(surface, 1, 0, "default")
        if type(default_animation) is not pygame.surface.Surface:
            return default_animation
        else:
            return Animation(default_animation, 1, 0, "default")

    def get_frame(self):
        if self.updated is True:
            return self.get_current_frame()
        self.updated = True
        if self.end_of_animation:
            self.animation_finished(cs.A_STOP_TIMER_EVENT)
        frame = self.original_frames[self.current_frame_id]
        frame_index = self.current_frame_id
        if self.current_frame_id == self.frames_cnt - 1 and self.playing_cnt >= 1:
            self.playing_cnt -= 1
        if self.playing_cnt == 0:
            self.playing_cnt = -1
            self.end_of_animation = True
        self.current_frame_id = (self.current_frame_id + 1) % self.frames_cnt
        return self.adapt_frame(frame, frame_index)

    def adapt_frame(self, frame, frame_index):
        if self.adapted_frame[frame_index] is False:
            frame = scale_image(self.application, frame, self.size, self.scale)
            frame = pygame.transform.flip(frame, self.symmetrically_y, self.symmetrically_x)
            frame = pygame.transform.rotate(frame, self.angle)
            self.adapted_frame[frame_index] = True
            self.frames[frame_index] = frame
        return self.frames[frame_index]

    def get_current_frame(self):
        return self.adapt_frame(self.original_frames[self.current_frame_id], self.current_frame_id)

    def get_active_animation(self) -> Animation:
        return self.animations[self.active_animation_id]

    def get_animation(self, animation_id) -> Animation:
        return self.animations[animation_id]

    def resize(self, size: np.array = np.array([None, None]), scale=None):
        self.scale = scale
        self.size = size
        self.adapted_frame = [False] * self.frames_cnt

    def set_setting(self, symmetrically_x=False, symmetrically_y=False):
        self.symmetrically_x = symmetrically_x
        self.symmetrically_y = symmetrically_y
        self.adapted_frame = [False] * self.frames_cnt

    def load_animation(self, animation_id, playing_time=None, playing_cnt=None):
        animation = self.get_animation(animation_id)
        self.angle = 0
        self.symmetrically_x = False
        self.symmetrically_y = False
        self.stop_animation_event = -1
        self.original_frames = animation.frames
        self.frames_cnt = animation.frames_cnt
        self.frames = [0] * self.frames_cnt
        self.end_of_animation = False
        self.adapted_frame = [False] * self.frames_cnt
        self.active_animation_id = animation.animation_id
        self.fps = animation.fps
        self.current_frame_id = 0
        self.resize(self.size, self.scale)
        if self.event_number != -1:
            self.application.delete_timer(self.event_number)
        if self.fps != 0:
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

    def update(self, events_list):
        for event in events_list:
            if event[0] == cs.E_EVENT:
                if event[1].type == pygame.USEREVENT + self.stop_animation_event:
                    self.application.delete_timer(self.stop_animation_event)
                    self.animation_finished(cs.A_STOP_TIMER_EVENT)
        self.updated = False

    def animation_finished(self, cause):
        self.load_default_animation()
        if self.connected_state_machine is not None:
            self.connected_state_machine.animation_finished({cs.A_ANIMATION_FINISHED_CAUSE: cause})

    def connect_state_machine(self, state_machine):
        self.connected_state_machine = state_machine
        self.animations[self.default_animation.animation_id] = self.init_default_animation(None)
        self.load_default_animation()
