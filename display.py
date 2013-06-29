import json, os

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from widget import Widget
from fileparser import FileParser

class TartanDisplay(object):

    def __init__(self, app, spec):
        self.app = app
        self.spec = spec
        self.widgets = []
        self.parser = FileParser(self.app)
        self.widgets = self.parser.parse(self.spec)
        self.canvas = Canvas(0, 0)
        self.display = Display(self.canvas)
        self.display.set_driver('gl')

    def refresh(self):

        self.build_display()
        self.display.refresh()

    def blit(self, widget):
        self.canvas.blit(widget.anchor[0], widget.anchor[1], widget.canvas)

    def build_display(self):
        self.canvas.clear()
        for widget in self.widgets:
            widget.draw()
            self.blit(widget)
