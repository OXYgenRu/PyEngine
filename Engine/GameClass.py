from collections import defaultdict

import pygame


class Game:
    def __init__(self, window_size, fps, start_scene):
        self.clock = None
        self.screen = None
        self.size = window_size
        self.fps = fps
        self.start_scene = start_scene
        self.scene = None
        self.scene_storage = defaultdict()
        self.font_storage = defaultdict()
        self.fonts_for_registration = []

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        running = True
        self.load_fonts()
        self.scene = self.start_scene(self.size[0], self.size[1], self)

        self.screen.fill((0, 0, 0))
        while running:
            tick_length = self.clock.tick(self.fps)
            self.screen.fill((0, 0, 0))
            self.scene.clear_surface()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.scene.update({"tick_length": tick_length})
            self.scene.render()
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

    def set_scene(self, scene_id):
        self.scene = self.scene_storage[scene_id](self.size[0], self.size[1], self)
