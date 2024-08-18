import numpy
import pygame.transform

from Engine.BasiсObjects import Polygon
from Engine.Colliders.UICollider import UICollider
from Engine.GameScene import GameScene
from Engine.RenderSurface import RenderSurface


class Menu(GameScene):
    def __init__(self, width, height, application):
        super().__init__(width, height, application)
        self.screen_space.set_filling('yellow')
        self.start_button = RenderSurface(self.screen_space, 0, 600, 400,
                                          numpy.array([width // 2 - 300, height // 2 - 300]))
        self.start_button.set_filling('green')
        self.rect = Polygon(self.start_button)
        self.rect.set_geometry(0, 0, 300, 300)
        self.button_collider = UICollider(self.start_button, numpy.array([[0, 0], [300, 0], [300, 300], [0, 300]]))
        self.button_collider.on_mouse_enter = self.uu
        self.button_collider.on_mouse_exit = self.uu1

    def uu(self):
        self.rect.color = 'blue'

    def uu1(self):
        self.rect.color = 'red'
