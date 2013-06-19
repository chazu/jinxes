import sys

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from display import TartanDisplay
from widget import Widget


class App:

    def __init__(self):
        self.display = TartanDisplay()
        self.digest_rate = 1000 #ms
        self.keypress_queue = []
        self.event_thing = Event()
        self.quit = False

    def process_events(self):
        if self.display.display.get_event(caca.EVENT_KEY_PRESS, self.event_thing, self.digest_rate):
            if self.event_thing.get_type() == caca.EVENT_KEY_PRESS:
                key = self.event_thing.get_key_ch()
                print "Processing key: " + str(key)
                # TODO: Widget instance whose callback is to be
                # called will need to be known by the event loop
                widget = self.display.widgets[0]

                if key == ord("q"):
                    self.quit = True
                if key == ord("j"):
                    if (widget.scroll["currentLine"] <
                        widget.scroll["maxCurrentLine"]):
                        widget.scroll["currentLine"] += 1
                if key == ord("k"):
                    if (widget.scroll["currentLine"] > 0):
                        widget.scroll["currentLine"] -= 1
                key=None

    def run(self):
        self.display.build_display()
        while self.quit == False:
            self.display.refresh()
            self.process_events()

app = App()
app.display.load_from_file('tui.json')

app.run()
