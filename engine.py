import sys

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

import json, os

class TartanDisplay(object):

    def __init__(self):
        self.canvas = Canvas(0, 0)
        self.display = Display(self.canvas)
        self.display.set_driver('gl')

    def refresh(self):
        self.display.refresh()


class Widget(object):

    def draw(self):
            self.canvas.put_str(self.text_origin[0],
                                self.text_origin[1],
                                self.text_buffer)

    def specifies(self, key, value=None):
        """
        True if the spec doc has the key.
        If value is passed in, True only
        if key is present and equal to value
        """
        return key in self.spec.keys() and (
            self.spec[key] == value if value != None else True)

    def border_builder(self):
        if self.specifies("border", True):
            print "drawing border"
            self.border = True
            self.canvas.draw_box(0, 0, self.spec["width"],
                                 self.spec["height"],"X")

    def text_buffer_builder(self):
        if self.specifies("text"):
            self.text_buffer = self.spec["text"]
        if self.specifies("border", True):
            self.text_origin = (1, 1)
        else:
            self.text_origin = (0, 0)

    def __init__(self, spec):
        self.spec = spec
        if self.specifies('name'):
            self.name = spec["name"]
        else:
            self.name = "Unknown"
        if self.specifies("height") and self.specifies("width"):
            print "creating canvas of specified size"
            self.canvas = Canvas(spec["width"],
                            spec["height"])
            self.canvas.set_color_ansi(caca.COLOR_RED, caca.COLOR_BLUE)
        else:
            print "creating generic size canvas"
            self.canvas = Canvas(0, 0)
            self.canvas.set_color_ansi(caca.COLOR_RED, caca.COLOR_BLUE)
        self.border_builder()
        self.text_buffer_builder()



config = json.load(open("tui.json"))
display = TartanDisplay()
widget = Widget(config)

widget.draw()
display.canvas.blit(0, 0, widget.canvas)
display.refresh()
display.display.get_event(caca.EVENT_KEY_PRESS, Event(), 99999999)
