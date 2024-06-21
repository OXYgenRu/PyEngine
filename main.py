import numpy
import pygame

import BasiсShapes
import RenderSurface

SIZE = WIDTH, HEIGHT = 1366, 768


class MainSurface(RenderSurface.RenderSurface):
    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT)
        self.pl = BasiсShapes.Polygon(self, numpy.array([[100, 100], [200, 100], [200, 200], [100, 200]]))
        self.surf = RenderSurface.RenderSurface(self, 2, 200, 200, numpy.array([100, 200]))
        self.pl1 = BasiсShapes.Polygon(self.surf, numpy.array([[50, 50], [100, 50], [200, 100], [50, 200]]))
        self.pl1.color = 'green'
        self.surf2 = RenderSurface.RenderSurface(self, 1, 600, 600, numpy.array([-200, -200]))
        self.pl12 = BasiсShapes.Polygon(self.surf2, numpy.array([[400, 400], [600, 400], [600, 600], [400, 600]]))
        self.pl12.color = 'blue'
        # self.surf.set_filling('red')


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    running = True
    ms = MainSurface()
    while running:
        ms.clear_surface()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ms.render()
        screen.blit(ms, (0, 0))
        pygame.display.flip()
    pygame.quit()
