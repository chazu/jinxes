import sys
import json, os

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from fileparser import FileParser
from display import TartanDisplay
from widget import Widget

config = json.load(open("tui.json"))
display = TartanDisplay()
parser = FileParser()

widgets = parser.parse(config)

for widget in widgets:
    display.widgets.append(widget)

display.build_display()
display.refresh()

display.display.get_event(caca.EVENT_KEY_PRESS, Event(), 99999999)
