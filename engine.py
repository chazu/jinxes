import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import json

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from display import TartanDisplay
from widget import Widget
import hooks
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

    def __init__(self, filename):
        self.spec = self.load_from_file(filename)
        self.display = TartanDisplay(self.spec["widgets"])
        self.local_event_dispatch = LocalEventDispatch()
        self.digest_rate = 1000 #ms
        self.keypress_queue = []
        self.event_thing = Event()
        self.quit = False

        # Keypress hooks
        self.keypress_hooks = []

        # Parse spec
        self.load_keypress_hooks()

    def load_keypress_hooks(self):
        for hook in self.spec["app"]["keyHooks"]:
            print hook
            self.register_keypress_hook(hook)

    def load_from_file(self, filepath):
        logging.debug("App loading filepath: " + str(filepath))
        return json.load(open(filepath))


    def register_keypress_hook(self, hook):
        self.keypress_hooks.append({"key": hook["key"],
                                    "func": getattr(hooks, hook["func"])})

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

app = App('tui.json')

# Focused widget (should be part of init
app.focused_widget = app.display.widgets[0]

app.run()
