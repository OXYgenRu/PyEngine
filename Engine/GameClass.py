import inspect
import os
import sys
from collections import defaultdict

import pygame
import Engine
import Engine.constants as cs


class Game:
    def __init__(self, window_size, fps, start_scene_id, init_file):
        self.game_folder = os.path.dirname(init_file)
        self.clock = None
        self.screen = None
        self.custom_event_counter = 0
        self.properties = Engine.PropertyStorage.PropertyStorage()
        self.size = window_size
        self.fps = fps
        self.start_scene_id = start_scene_id
        self.scene = None
        self.scene_storage = defaultdict()
        self.loaded_scene_storage = defaultdict(None)
        self.font_storage = defaultdict()
        self.fonts_for_registration = []
        self.init_properties()
        self.timers = defaultdict(bool)
        print(self.game_folder)

    def init_properties(self):
        self.properties.update(cs.P_SCALING_TYPE, cs.P_SCALING_TYPE_PYGAME)

    def set_property(self, property_name, value):
        self.properties.update(property_name, value)

    def get_property(self, property_name):
        return self.properties.get(property_name)

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        running = True
        self.load_fonts()
        self.set_new_scene(self.start_scene_id)

        self.screen.fill((0, 0, 0))
        while running:
            tick_length = self.clock.tick(self.fps)
            self.screen.fill((0, 0, 0))
            self.scene.clear_surface()
            for event in pygame.event.get():
                self.scene.update({"event": event})
                if event.type == pygame.QUIT:
                    running = False
            self.scene.update({"tick_length": tick_length})
            self.scene.render()
            # self.rscene = pygame.transform.scale(self.scene, (self.size[0] * 0.5, self.size[1] * 0.5))
            self.screen.blit(self.scene, (0, 0))
            pygame.display.flip()
        pygame.quit()

    def load_fonts(self):
        pygame.font.init()
        self.font_storage["arial_23"] = pygame.font.SysFont('Arial', 23)
        for content in self.fonts_for_registration:
            self.font_storage[content[2]] = pygame.font.SysFont(content[0], content[1])

    def register_scene(self, scene_like_class, scene_id):
        self.scene_storage[scene_id] = scene_like_class

    def register_font(self, font_name, font_size, font_id):
        self.fonts_for_registration.append((font_name, font_size, font_id))

    def set_new_scene(self, scene_id):
        self.scene = self.scene_storage[scene_id](self.size[0], self.size[1], self)
        self.loaded_scene_storage[scene_id] = self.scene

    def load_scene(self, scene_id):
        self.scene = self.loaded_scene_storage[scene_id]

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(self.game_folder, os.path.join('data', name))
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def set_timer(self, period):
        index = 1
        while index < 1000:
            if self.timers[index] is False:
                self.timers[index] = True
                pygame.time.set_timer(pygame.USEREVENT + index, period)
                break
            index += 1
        return index

    def delete_timer(self, event_id):
        self.timers[event_id] = False
        pygame.time.set_timer(pygame.USEREVENT + event_id, 0)
