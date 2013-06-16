import json, os

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from widget import Widget
from fileparser import FileParser

class TartanDisplay(object):

    def __init__(self):
        self.canvas = Canvas(0, 0)
        self.display = Display(self.canvas)
        self.display.set_driver('gl')
        self.widgets = []
        self.parser = FileParser()
    def refresh(self):
        self.display.refresh()

    def blit(self, widget):
        self.canvas.blit(widget.anchor[0], widget.anchor[1], widget.canvas)

    def build_display(self):
        for widget in self.widgets:
            widget.draw()
            self.blit(widget)

    def load_from_file(self, filepath):
        config = json.load(open(filepath))
        self.widgets = self.parser.parse(config)
