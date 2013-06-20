import sys

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from display import TartanDisplay
from widget import Widget

class LocalEventDispatch:
    """
    Takes events from inside of the engine (caca events
    such as keypresses), matches them to widgets
    and executes callbacks which affect widgets.

    Mapping of events to widgets is established at
    instance initialization based on the specification
    document used to construct the UI.
    TODO: Since both this class and TartanDisplay use
    the spec, pass it into both constructors
    """

    def __init__(self):
        """
        Parse the spec and create mappings to various
        functions that will affect UI state
        """
        pass

    def dispatch_events(self, events):
        """
        Do your magic: tell widgets what to do
        """
        pass


class App:

    defaultAppState = {
        "focus":{
            "wrap": False
        },
        "size": "auto",
        "keys": [{"q":"quitApp"}],
    }

    def __init__(self):
        self.display = TartanDisplay()
        self.local_event_dispatch = LocalEventDispatch()
        self.digest_rate = 1000 #ms
        self.keypress_queue = []
        self.event_thing = Event()
        self.quit = False

        # Keypress hooks
        self.keypress_hooks = []

    def register_keypress_hook(self, hook):
        self.keypress_hooks.append(hook)

    def get_handler_for_key(self, key):
        print key
        res = filter(lambda hook: ord(hook["key"]) == key, self.keypress_hooks)
        return res

    def process_events(self):
        if self.display.display.get_event(caca.EVENT_KEY_PRESS, self.event_thing, self.digest_rate):
            if self.event_thing.get_type() == caca.EVENT_KEY_PRESS:

                key = self.event_thing.get_key_ch()
                if key in [ord(hook["key"]) for hook in self.keypress_hooks]:
                    hook = self.get_handler_for_key(key)
                    print hook
                    hook[0]["func"](self)
                key=None

    def run(self):
        self.display.build_display()
        while self.quit == False:
            self.display.refresh()
            self.process_events()

## Keypress Functions ###################################

def quitApp(app):
    app.quit = True

def scrollFocusDown(app):
    if (app.focused_widget.scroll["currentLine"] <
        app.focused_widget.scroll["maxCurrentLine"]):
        app.focused_widget.scroll["currentLine"] += 1

def scrollFocusUp(app):
    if (app.focused_widget.scroll["currentLine"] > 0):
        app.focused_widget.scroll["currentLine"] -= 1

#########################################################

app = App()
app.display.load_from_file('tui.json')
# Focused widget (should be part of init
app.focused_widget = app.display.widgets[0]

app.register_keypress_hook({"key":"q",
                            "func":quitApp})
app.register_keypress_hook({"key": "j",
                            "func": scrollFocusDown})
app.register_keypress_hook({"key": "k",
                            "func": scrollFocusUp})
app.run()
