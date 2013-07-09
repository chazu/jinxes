import logging
import argparse
import sys
import json

from display import TartanDisplay
from local_event_dispatch import LocalEventDispatch
from remote_event_dispatch import RemoteEventDispatch

import caca
from caca.display import Display, DisplayError, Event
import hooks

class App:

    defaultColorMap = {
        "black"        : 0,
        "blue"         : 1,
        "green"        : 2,
        "cyan"         : 3,
        "red"          : 4,
        "magenta"      : 5,
        "brown"        : 6,
        "lightgray"    : 7,
        "darkgray"     : 8,
        "lightblue"    : 9,
        "lightgreen"   : 10,
        "lightcyan"    : 11,
        "lightred"     : 12,
        "lightmagenta" : 13,
        "yellow"       : 14,
        "white"        : 15
        }

    defaultStyles = [
        {
            "name": "default",
            "bgColor": "black",
            "fgColor": "white"
            }
        ]

    defaultAppState = {
        "styles": defaultStyles,
        "app":
            {
            "keyHooks":
                [
                {
                    "key": "q",
                    "func": "quitApp"
                    }
                ],
            "height": 24,
            "width": 80
            },
        "widgets": []
        }

    def __init__(self, filename=None):
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--inittest",
                                     help="Initialize app and quit",
                                     action="store_true",
                                     default=False)
        self.arg_parser.add_argument("--loglevel",
                                 help="DEBUG, INFO or WARN",
                                 default="debug")
        self.args = self.arg_parser.parse_args()

        logging.basicConfig(level=getattr(logging, self.args.loglevel))

        self.initialize_app_spec(filename)
        print "FINAL SPEC"
        print str(self.spec)
        self.display = TartanDisplay(self, self.spec)
        self.local_event_dispatch = LocalEventDispatch()
        self.digest_rate = 1000 #ms
        self.keypress_queue = []
        self.event_thing = Event()
        self.quit = False
        self.styles = []

        # Keypress hooks
        self.keypress_hooks = []

        # Parse spec
        self.load_keypress_hooks()
        self.load_styles()

        # Start consuming remote messages

        self.remote_messages = []
        self.remote_dispatch = RemoteEventDispatch("tartan", self)
        self.remote_dispatch.init_consume()

    def process_style(self, style):
        """
        Given a hash representing a style, convert
        to a format usable by the engine, i.e.
        convert color names to caca values
        """
        logging.debug("Loading App Style " + style["name"])
        color_mapped_style = {
            "name": style["name"],
            "fgColor": App.defaultColorMap[style["fgColor"]],
            "bgColor": App.defaultColorMap[style["bgColor"]],
            }
        if "reverse" in style.keys():
            color_mapped_style["reverse"] = style["reverse"]
        logging.debug("Color mapped style:")
        logging.debug(str(color_mapped_style))
        return color_mapped_style

    def load_styles(self):
        for style in self.spec["styles"]:
            self.styles.append(self.process_style(style))
        logging.debug("Final styles for app:")
        logging.debug(str(self.styles))

    def load_keypress_hooks(self):
        for hook in self.spec["app"]["keyHooks"]:
            print hook
            self.register_keypress_hook(hook)

    def initialize_default_app_spec(self):
        logging.info("Initialized default app spec")
        self.spec = App.defaultAppState.copy()
        logging.debug("default spec: " + str(self.spec))

    def initialize_app_spec(self, filepath):
        self.initialize_default_app_spec()
        if filepath != None:
            logging.info("App loading filepath: " + str(filepath))
            loaded_spec = json.load(open(filepath))
            logging.debug("Loaded spec: " + str(loaded_spec))
            self.spec.update(loaded_spec)
            logging.debug("Updated spec: " + str(self.spec))

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
        if self.args.inittest != True:
            while self.quit == False:
                self.display.refresh()
                self.process_events()
                self.remote_dispatch.check_queue()
