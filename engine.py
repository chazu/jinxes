import sys

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

import json, os

config = json.load(open("tui.json"))

cv = Canvas(0, 0)
dp = Display(cv)
dp.set_driver('gl')


# cv.put_str(0, 0, config["text"])
# dp.get_event(caca.EVENT_KEY_PRESS, Event(), 99999999)
# dp.refresh()

def parse(tui):
    if "width" in tui.keys() and "height" in tui.keys():
        print "creating canvas of specified size"
        canvas = Canvas(tui["width"],
                        tui["height"])
        canvas.set_color_ansi(caca.COLOR_RED, caca.COLOR_BLUE)
    else:
        print "creating generic size canvas"
        canvas = Canvas(0, 0)
        canvas.set_color_ansi(caca.COLOR_RED, caca.COLOR_BLUE)
    if "border" in tui.keys() and tui["border"] == True:
        print "drawing border"
        canvas.draw_box(0, 0, tui["width"],
                        tui["height"],"X")
    if "text" in tui.keys():
        print "drawing text: " + tui["text"]
        canvas.put_str(0, 0, tui["text"])
    return canvas

widget = parse(config)
print "Widget: " + str(widget)
cv.blit(0, 0, widget)
dp.refresh()
dp.get_event(caca.EVENT_KEY_PRESS, Event(), 99999999)
