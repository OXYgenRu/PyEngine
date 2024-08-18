import numpy
import pygame.event
from shapely import Polygon, Point

from Engine import GameClass


class UICollider:
    def __init__(self, render_surface, points: numpy.array):
        self.points = points
        self.render_surface = render_surface
        self.mouse_entered = False
        self.application: GameClass = render_surface.application
        self.render_surface.colliders.append(self)

    def mouse_event_update(self, mouse_event: pygame.event.Event, mouse_pos) -> bool:
        if not Point(mouse_pos).intersects(Polygon(self.points.tolist())):
            return False
        if mouse_event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_down(mouse_event.button)
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            self.on_mouse_up(mouse_event.button)
        if mouse_event.type == pygame.MOUSEMOTION and self.mouse_entered is False:
            self.on_mouse_enter()
            self.mouse_entered = True
            self.application.ui_collider_system.active_entered_ui_collider = self
        return True

    def on_mouse_enter(self):
        pass

    def on_mouse_exit(self):
        pass

    def on_mouse_down(self, button):
        pass

    def on_mouse_up(self, button):
        pass

    def on_mouse_over(self):
        pass


class UIColliderSystem:
    def __init__(self, application):
        self.active_entered_ui_collider = None
        self.mouse_collide = None
        self.application = application

    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP
                or event.type == pygame.MOUSEMOTION):
            result = self.application.scene.update_ui_colliders(event, event.pos)
            if self.mouse_collide is None or self.mouse_collide is False:
                self.mouse_collide = result

    def update_colliders(self):
        if self.mouse_collide is False:
            if self.active_entered_ui_collider is not None:
                self.active_entered_ui_collider.mouse_entered = False
                self.active_entered_ui_collider.on_mouse_exit()
                self.active_entered_ui_collider = None
        self.mouse_collide = None
        if self.active_entered_ui_collider is not None:
            self.active_entered_ui_collider.on_mouse_over()
