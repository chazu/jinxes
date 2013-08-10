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

        # Parse command line arguments
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--inittest",
                                     help="Initialize app and quit",
                                     action="store_true",
                                     default=False)
        self.arg_parser.add_argument("--loglevel",
                                 help="DEBUG, INFO or WARN",
                                 default="debug")
        self.args = self.arg_parser.parse_args()

        # Configure logging TODO: Use one logger object everywhere
        logging.basicConfig(level=getattr(logging, self.args.loglevel))

        # Initialize Spec/State
        self.initialize_app_spec(filename)
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
        hook["func"] = getattr(hooks, hook["func"])

    def get_handler_for_key(self, key):
        res = filter(lambda hook: ord(hook["key"]) == key, self.keypress_hooks)
        return res

    def get_widget_hook_for_key(self, key):
        """
        Return the widget and relevant hook for the key
        """
        res = [widget.get_keyhook_for(key) for widget in self.display.widgets]
        res = filter(lambda x: x != None,
                     res)
        return res[0] if len(res) > 0 else None

    def get_focused_widget_hook_for_key(self, key):
        """
        TODO write this docstring
        """
        return self.display.focused_widget.get_focused_keyhook_for(key)

    def get_focused_widget_catchall_hook(self):
        return self.display.focused_widget.get_focused_keyhook_for("ALL")

    def get_hook_for_key(self, key):
        """
        Get app hook for key
        """
        res = filter(lambda x: x["key"] == key,
                     self.spec["app"]["keyHooks"])
        if len(res) > 0:
            res = res[0]
        else:
            res = None
        return res

    def process_events(self):
        if self.display.display.get_event(caca.EVENT_KEY_PRESS, self.event_thing, self.digest_rate):
            if self.event_thing.get_type() == caca.EVENT_KEY_PRESS:
                key = chr(self.event_thing.get_key_ch())

                hook = self.get_hook_for_key(key)
                if hook != None:
                    hook["func"](self)
                else:
                    hook = self.get_focused_widget_hook_for_key(key)
                    if hook != None:
                        hook["func"](hook["widget"])
                        # Execute hook for widget
                    else:
                        hook = self.get_widget_hook_for_key(key)

                        if hook != None:
                            # execute the hook
                            hook["func"](hook["widget"])
                        else:
                            hook = self.get_focused_widget_catchall_hook()
                            if hook != None:
                                hook["func"](hook["widget"])
                # TODO: Else run unhandled_input hook
                key=None # Reset key

    def run(self):
        self.display.build_display()
        if self.args.inittest != True:
            while self.quit == False:
                self.display.refresh()
                self.process_events()
                self.remote_dispatch.check_queue()
