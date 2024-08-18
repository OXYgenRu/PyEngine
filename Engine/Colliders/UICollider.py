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
            self.application.ui_collider_system.active_clicked_ui_collider = self
            self.on_mouse_up(mouse_event.button)
        if mouse_event.type == pygame.MOUSEMOTION:
            if self.mouse_entered is False:
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
        self.active_clicked_ui_collider = None

        self.on_mouse_button_down_collide = None
        self.on_mouse_button_up_collide = None
        self.on_mouse_button_motion_collide = None
        self.on_mouse_button_wheel_motion_collide = None
        self.application = application

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button != 4 and event.button != 5:
            pos = numpy.array([event.pos[0], event.pos[1]])
            result = self.application.scene.update_ui_colliders(event, pos)
            if self.on_mouse_button_down_collide is None or self.on_mouse_button_down_collide is False:
                self.on_mouse_button_down_collide = result
        if event.type == pygame.MOUSEBUTTONUP and event.button != 4 and event.button != 5:
            pos = numpy.array([event.pos[0], event.pos[1]])
            result = self.application.scene.update_ui_colliders(event, pos)
            if self.on_mouse_button_up_collide is None or self.on_mouse_button_up_collide is False:
                self.on_mouse_button_up_collide = result
        if event.type == pygame.MOUSEMOTION:
            pos = numpy.array([event.pos[0], event.pos[1]])
            result = self.application.scene.update_ui_colliders(event, pos)
            if self.on_mouse_button_motion_collide is None or self.on_mouse_button_motion_collide is False:
                self.on_mouse_button_motion_collide = result

    def update_colliders(self):
        if self.on_mouse_button_motion_collide is False:
            if self.active_entered_ui_collider is not None:
                self.active_entered_ui_collider.mouse_entered = False
                self.active_entered_ui_collider.on_mouse_exit()
                self.active_entered_ui_collider = None
        if self.on_mouse_button_up_collide is False:
            if self.active_clicked_ui_collider is not None:
                self.active_clicked_ui_collider = None
        if self.active_entered_ui_collider is not None:
            self.active_entered_ui_collider.on_mouse_over()
        self.on_mouse_button_down_collide = None
        self.on_mouse_button_up_collide = None
        self.on_mouse_button_motion_collide = None
