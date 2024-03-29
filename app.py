import logging
import argparse
import json

from display import TartanDisplay
from local_event_dispatch import LocalEventDispatch
from remote_event_dispatch import RemoteEventDispatch
from util import multiIndex, isDict

import caca
from caca.display import Event
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
                "remoteMessages":
                {
                    "queues": []
                },
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

    def specifies(self, key, value=None, path=None):
        spec_doc = self.spec
        try:
            if path != None and isDict(multiIndex(spec_doc, path)):
                target = multiIndex(spec_doc, path)
                if value == None:
                    return key in target.keys()
                else:
                    return target[key] == value
            else:
                target = self.spec
                return key in target.keys() and (
                    target[key] == value if value != None else True)
        except KeyError:
            self.logger.warn("Key error when requesting path " + \
                                 str(path) + " for app")
            return False

    def __init__(self, filename=None):

        # Parse command line arguments
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--inittest",
                                     help="Initialize app and quit",
                                     action="store_true",
                                     default=False)
        self.arg_parser.add_argument("--loglevel",
                                 help="DEBUG, INFO or WARN",
                                 default="DEBUG")
        self.arg_parser.add_argument("--driver",
                                     action="store",
                                     dest="driver",
                                     default="gl",
                                     help="Select display driver: gl, curses, slang")
        self.args = self.arg_parser.parse_args()

        self.logger = logging.getLogger()
        self.logger.setLevel(self.args.loglevel)

        # Initialize Spec/State
        self.initialize_app_spec(filename)
        logging.debug("USING DRIVER: " + self.args.driver)
        if self.args.driver:
            self.display = TartanDisplay(self, self.spec, self.args.driver)
        else:
            self.display = TartanDisplay(self, self.spec)
        self.local_event_dispatch = LocalEventDispatch(self)
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

        # Initialize network connection IF specified
        if self.specifies("network", True, ["app"]):
            self.remote_messages = []
            self.remote_dispatch = RemoteEventDispatch(self)
            self.remote_dispatch.init_consume()

    def process_style(self, style):
        """
        Given a hash representing a style, convert
        to a format usable by the engine, i.e.
        convert color names to caca values
        """
        self.logger.debug("Loading App Style " + style["name"])
        color_mapped_style = {
            "name": style["name"],
            "fgColor": App.defaultColorMap[style["fgColor"]],
            "bgColor": App.defaultColorMap[style["bgColor"]],
            }
        if "reverse" in style.keys():
            color_mapped_style["reverse"] = style["reverse"]
        self.logger.debug("Color mapped style:")
        self.logger.debug(str(color_mapped_style))
        return color_mapped_style

    def load_styles(self):
        for style in self.spec["styles"]:
            self.styles.append(self.process_style(style))
        self.logger.debug("Final styles for app:")
        self.logger.debug(str(self.styles))

    def load_keypress_hooks(self):
        for hook in self.spec["app"]["keyHooks"]:
            self.register_keypress_hook(hook)

    def initialize_default_app_spec(self):
        self.logger.info("Initialized default app spec")
        self.spec = App.defaultAppState.copy()
        self.logger.debug("default spec: " + str(self.spec))

    def initialize_app_spec(self, filepath):
        self.initialize_default_app_spec()
        if filepath != None:
            self.logger.info("App loading filepath: " + str(filepath))
            loaded_spec = json.load(open(filepath))
            self.logger.debug("Loaded spec: " + str(loaded_spec))
            self.spec.update(loaded_spec)
            self.logger.debug("Updated spec: " + str(self.spec))

    def register_keypress_hook(self, hook):
        hook["func"] = getattr(hooks, hook["func"])

    def get_widget_hook_for_key(self, key):
        """
        Return the widget and relevant hook for the key
        """
        res = [widget.get_keyhook_for(key) for widget in self.display.widgets]
        res = filter(lambda x: x != None,
                     res)
        return res[0] if len(res) > 0 else None

    def get_focused_widget_hook_for_key(self, key):
        return self.display.focused_widget.get_focused_keyhook_for(key)

    def get_focused_widget_catchall_hook(self):
        return self.display.focused_widget.get_focused_keyhook_for("ALL")

    def get_hook_for_key(self, key):
        res = filter(lambda x: x["key"] == key,
                     self.spec["app"]["keyHooks"])
        if len(res) > 0:
            res = res[0]
        else:
            res = None
        return res

    def process_messages(self, msg_type="remote"):
        message_collection = self.remote_messages if msg_type == \
            "remote" else self.local_event_dispatch.messages

        for message in message_collection:
            for widget in self.display.widgets:
                hook = widget.get_message_hook_for_channel(message["channel"],
                                                           msg_type=msg_type)
                if hook:
                    hook["func"](widget, message=message)
            message_collection.remove(message)

    def process_keypresses(self):
        if self.display.display.get_event(caca.EVENT_KEY_PRESS,
                                          self.event_thing,
                                          self.digest_rate):
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
                                hook["func"](hook["widget"], key=key)
                # TODO: Else run unhandled_input hook
                key = None # Reset key

    def run(self):
        self.display.build_display()
        if self.args.inittest != True:
            while self.quit == False:
                self.display.refresh()
                self.process_keypresses()
                if self.specifies("network", True, ["app"]):
                    self.process_messages()
                    self.process_messages(msg_type="local")
                    self.remote_dispatch.check_queue()
