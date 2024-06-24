import numpy
import pygame

import Engine.BasiсShapes
import Engine.RenderSurface
import Engine.GameClass
import Engine.GameScene

SIZE = WIDTH, HEIGHT = 1366, 768


class MainScene(Engine.GameScene.GameScene):
    def __init__(self, width, height, application):
        super().__init__(width=width, height=height, application=application)
        self.pl = Engine.BasiсShapes.Polygon(self, numpy.array([[100, 100], [200, 100], [200, 200], [100, 200]]))
        self.surf = Engine.RenderSurface.RenderSurface(self, 2, 200, 200, numpy.array([100, 200]))
        self.pl1 = Engine.BasiсShapes.Polygon(self.surf, numpy.array([[50, 50], [100, 50], [200, 100], [50, 200]]))
        self.pl1.color = 'green'
        self.surf2 = Engine.RenderSurface.RenderSurface(self, 1, 600, 600, numpy.array([-200, -200]))
        self.pl12 = Engine.BasiсShapes.Polygon(self.surf2,
                                               numpy.array([[400, 400], [600, 400], [600, 600], [400, 600]]))
        self.pl12.color = 'blue'


class SecondScene(Engine.GameScene.GameScene):
    def __init__(self, width, height, application):
        super().__init__(width=width, height=height, application=application)
        # self.fill_color = 'red'
        self.sr1 = Engine.RenderSurface.RenderSurface(self, 2, 200, 200, numpy.array([100, 100]))
        self.sr2 = Engine.RenderSurface.RenderSurface(self, 3, 200, 200, numpy.array([150, 100]))
        self.sr1.add_border()
        self.sr2.add_border()
        # self.sr2.hide()
        self.cr = Engine.BasiсShapes.Circle(self.sr1, numpy.array([[100, 100], [150, 150]]))
        self.tx = Engine.BasiсShapes.Text(self.sr2, numpy.array([100, 100]),
                                          'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', font_id='arial_40',
                                          color='green')


if __name__ == '__main__':
    game = Engine.GameClass.Game((1366, 765), 10, SecondScene)
    game.register_scene(SecondScene, '1')
    game.register_scene(MainScene, '2')
    game.register_font('Arial', 40, 'arial_40')
    game.start()
