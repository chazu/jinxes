import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from widget import Widget

class TartanDisplay(object):

    def __init__(self):
        self.canvas = Canvas(0, 0)
        self.display = Display(self.canvas)
        self.display.set_driver('gl')
        self.widgets = []

    def refresh(self):
        self.display.refresh()

    def blit(self, widget):
        self.canvas.blit(widget.anchor[0], widget.anchor[1], widget.canvas)

    def build_display(self):
        for widget in self.widgets:
            widget.draw()
            self.blit(widget)
