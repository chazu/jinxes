import sys

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from display import TartanDisplay
from widget import Widget

class App:

    def __init__(self):
        self.display = TartanDisplay()

    def run(self):
        self.display.build_display()
        while 1:
            self.display.refresh()
            self.display.display.get_event(caca.EVENT_KEY_PRESS, Event(), 99999999)

app = App()
app.display.load_from_file('tui.json')

app.run()


