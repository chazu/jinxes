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

    def specifies(self, spec, key, value=None):
        """
        True if the spec doc has the key.
        If value is passed in, True only
        if key is present and equal to value
        """
        return key in spec.keys() and (
            spec[key] == value if value != None else True)

    def update(self):
        pass

    def border_builder(self, spec):
        print str(spec["border"])
        if self.specifies(spec, "border", True):
            print "drawing border"
            self.border = True
            self.canvas.draw_box(0, 0, spec["width"],
                                 spec["height"],"X")

    def __init__(self, spec):
        if "width" in spec.keys() and "height" in spec.keys():
            print "creating canvas of specified size"
            self.canvas = Canvas(spec["width"],
                            spec["height"])
            self.canvas.set_color_ansi(caca.COLOR_RED, caca.COLOR_BLUE)
        else:
            print "creating generic size canvas"
            self.canvas = Canvas(0, 0)
            self.canvas.set_color_ansi(caca.COLOR_RED, caca.COLOR_BLUE)
        self.border_builder(spec)
        if "text" in spec.keys():
            print "drawing text: " + spec["text"]
            self.canvas.put_str(1, 1, spec["text"])


config = json.load(open("tui.json"))
display = TartanDisplay()
widget = Widget(config)

display.canvas.blit(0, 0, widget.canvas)
display.refresh()
display.display.get_event(caca.EVENT_KEY_PRESS, Event(), 99999999)
