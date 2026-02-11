from . import config as conf

class Geometry:
    height_ratio = conf.HEIGHT_RATIO
    aspect_ratio = conf.ASPECT_RATIO

    window_width = None
    window_height = None
    x = None
    y = None

    def whp(self, percent):
        return int(self.window_height * percent / 100)


geometry = Geometry()
