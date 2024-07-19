import numpy

import Engine.RenderSurface


class Camera(Engine.RenderSurface.RenderSurface):
    def __init__(self, display_surface, camera_setting: numpy.array = numpy.array([0, 0, 1]), parent_surface=None,
                 render_priority=None, width=None, height=None,
                 transfer_vector: numpy.array = numpy.array([0, 0])):
        super().__init__(parent_surface, render_priority, width, height, transfer_vector)
        # camera_setting[0] - x_pos
        # camera_setting[0] - y_pos
        # camera_setting[0] - zoom
        self.display_surface = display_surface
        self.camera_setting = camera_setting

    # def render(self):
    #     if self.properties.get("hided"):
    #         return
    #     self.fill(self.fill_color)
    #     transfer_vector =
