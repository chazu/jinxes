import time
from copy import copy
import logging

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

from util import *

class Widget(object):

    # Default json structures for nested instance config info
    # Note that simple base-level data will just be stored in
    # instance attributes without default attr dicts to override

    defaultBorderAttributes = {
        "present": True,
        "visible": True,
        "character": "X",
        "style": "default"
        }

    defaultScrollingAttributes = {
        "scroll": False,
        "currentLine": 0
        }

    # Specification and lookup methods
    # --------------------------------
    # These methods are used to query the widget's spec
    # or current_state, and to conveniently retrieve
    # values from app-level styles

    def get_spec_doc(self, check_against_spec):
        """
        Helper method.
        Return the spec or the current state, as the situation
        requires
        """
        return (self.current_state if check_against_spec == False
                    else self.spec)

    def specifies(self, key, value=None, path=None, check_against_spec=False):
        """
        Key - The key to search for
        Value - A value to check equality for
        Path - The path in the spec to search
        check_against_state - True if you want to look at self.current_state
        instead of self.spec

        Returns ->
        True if the spec doc has the key.
        If value is passed in, True only
        if key is present and equal to value
        """
        spec_doc = self.get_spec_doc(check_against_spec)
        try:
            if path != None and isDict(multiIndex(spec_doc, path)):
                target = multiIndex(spec_doc, path)
                # logging.debug("Specification found: ")
                # logging.debug("Key   : " + key)
                # logging.debug("path  : " + str(path))
                # logging.debug("value: " + str(target))
                if value == None:
                    return key in target.keys()
                else:
                    return target[key] == value
            else:
                target = self.spec
                # logging.debug("Specification found: ")
                # logging.debug("Key         : " + key)
                # logging.debug("equals value: " + str(value))
                # logging.debug("at spec path: " + str(path))
                return key in target.keys() and (
                    target[key] == value if value != None else True)
        except KeyError:
            logging.warn("Key error when requesting path " + \
                str(path) + " for widget " + self.name)
            return False

    def specifies_not_equal(self, key, value, check_against_spec=False):
        """
        True if the value is specified but not equal to given value
        """
        spec_doc = self.get_spec_doc(check_against_spec)
        return spec_doc[key] != value

    def get_style_for_spec_section(self,
                                   style_target,
                                   check_against_spec=False):
        """
        Return the style hash for a section of the spec
        such as "contents" or "border"
        """
        spec_doc = self.get_spec_doc(check_against_spec)
        name = spec_doc[style_target]["style"]
        return filter(lambda x: x["name"] == name , self.app.styles)[0]

    def style_value_for(self, style_target, value, check_against_spec=False):
        """
        Lookup the relevant style stored in the app-level spec
        style_target - the portion of the widget's spec
        which contains the style, e.g. "border"
        value - the specific style portion we want: foreground,
        background, etc.
        """
        # TODO We should cache these values on widget init, so we dont
        # look them up every time we draw a damn widget
        spec_doc = self.get_spec_doc(check_against_spec)
        # logging.debug("Looking up style " + spec_doc[style_target]["style"] \
        #                   + " for target " + style_target)
        style_name = spec_doc[style_target]["style"]
        style = filter(lambda x: x["name"] == style_name,
                       self.app.styles)[0]
        # logging.debug("Got App style: " + str(style))
        color_value_for_style_element = style[value]
        # logging.debug("got style value: " + str(color_value_for_style_element))
        return color_value_for_style_element

    def style_specifies(self,
                        style_target,
                        element,
                        value=None,
                        check_against_spec=False):
        style = self.get_style_for_spec_section(style_target,
                                                check_against_spec)
        if value == None:
            return element in style.keys()
        else:
            return element in style.keys() and style[element] == value

    def set_canvas_color_per_style_for(self, style_target):
        if self.style_specifies(style_target, "reverse", True):
            self.canvas.set_color_ansi(
                self.style_value_for(style_target, "bgColor"),
                self.style_value_for(style_target, "fgColor"))
        else:
            self.canvas.set_color_ansi(
                self.style_value_for(style_target, "fgColor"),
                self.style_value_for(style_target, "bgColor"))


    # Drawing methods
    # ---------------------------
    # Actual manipulation of the widget canvas goes here
    ###############################################################

    def draw_line_buffer(self):
        line_start = copy(self.text_origin)
        self.set_canvas_color_per_style_for("contents")
        for line in self.get_visible_slice():
            self.canvas.put_str(line_start[0],
                                line_start[1],
                                line)
            line_start[1] += 1

    def draw_border(self):
        if self.specifies("border"):
            char = self.border["character"]
            self.set_canvas_color_per_style_for("border")
            self.canvas.draw_box(0, 0, self.current_state["width"],
                                 self.current_state["height"],str(char))

    def draw(self):
        """
        This is called once every time through the main loop.
        Dirty widgets are rebuilt in here.
        """
        if self.dirty:
            self.build_all()
            self.mark_clean()

        self.canvas.clear()
        self.draw_line_buffer()
        self.draw_border()

    # Builder methods - take the spec for the widget and build out
    # instance state
    ###############################################################

    def border_builder(self):
        if self.specifies("border") and isDict(self.current_state["border"]):
            self.border = Widget.defaultBorderAttributes.copy()
            self.border.update(self.current_state["border"])
        else:
            self.border = Widget.defaultBorderAttributes.copy()

    def line_buffer_builder(self):
        """
        Update internal line buffer based on dimensions
        of widget, border and length of text contents

        Call this after resize
        """
        draw_width = (self.current_state["width"] - 2 if self.specifies("border") else self.width)
        self.line_buffer = chunks(self.text_buffer, draw_width)
        # Dont allow scrolling beyond end of line buffer
        self.scroll["maxCurrentLine"] = len(self.line_buffer)

    def text_buffer_builder(self):
        # logging.debug("Calling text buffer builder for " + self.name)
        if self.specifies("text", path=["contents"]):
            # logging.debug("Setting text buffer for widget " + self.name)
            self.text_buffer = self.current_state["contents"]["text"]
        if self.specifies("border"):
            self.text_origin = [1, 1]
        else:
            self.text_origin = [0, 0]

    def anchor_builder(self):
        if self.specifies("anchor"):
            self.anchor = self.current_state["anchor"]
        else:
            self.anchor = (0, 0)

    def visible_slice_builder(self):
        """
        initialize or change visible slice
        """
        if self.border["present"]:
            self.visible_lines = self.current_state["height"] - 2
        else:
            self.visible_lines = self.current_state["height"]

    def scroll_builder(self):
        """
        Build/Initialize state related to scrolling capabilities and
        behavior
        """
        # set up scrolling
        if self.specifies("scroll"):
            self.scroll = Widget.defaultScrollingAttributes.copy()
            self.scroll.update(self.current_state["scroll"])
        else:
            self.scroll = Widget.defaultScrollingAttributes.copy()

    def build_all(self):
        self.anchor_builder()
        self.border_builder()
        self.scroll_builder()
        self.text_buffer_builder()
        self.line_buffer_builder()
        self.visible_slice_builder()

    def update_scroll_current_line(self, delta):
        self.scroll["currentLine"] += int(delta)

    def get_visible_slice(self):
        """
        return visible segment of line buffer
        """
        start = self.scroll["currentLine"]
        end = start + self.visible_lines
        res = self.line_buffer[start:]
        res = res[:end]
        return res

    def initialize_spec_and_state(self, spec):
        """
        Spec should always be the initial spec
        Cached state represents a layer of 'undo' if you will,
        while current state is what is used to build and draw
        """
        self.spec = spec
        self.cached_state = spec.copy()
        self.current_state = spec.copy()

        self.current_state["custom"] = {}
        self.cached_state["custom"] = {}

    def resize(self, height, width):
        # TODO Cache keys before changing them
        self.cache_state_at_path(["width"])
        self.cache_state_at_path(["height"])

        self.current_state["width"] = width
        self.current_state["height"] = height
        self.canvas.set_size(width, height)
        self.app.display.mark_dirty()

    def move_anchor(self, row, column):
        self.current_state["anchor"] = (row, column)
        self.app.display.mark_dirty()

    def cache_state_at_path(self, path_array):
        """
        Given a path into the current state, store the value
        found there in the cache
        """
        value_to_cache = multiIndex(self.current_state, path_array)
        multiIndexAssign(self.cached_state, path_array, value_to_cache)

    def restore_state_from_cache(self, path_array):
        """
        Given a path into the cached state, restore the value
        found there to the current state
        """
        value_to_restore = multiIndex(self.cached_state, path_array)
        multiIndexAssign(self.current_state, path_array, value_to_restore)

    def mark_dirty(self):
        self.dirty = True

    def mark_clean(self):
        self.dirty = False

    def __init__(self, app, spec):
        self.app = app
        self.initialize_spec_and_state(spec)
        self.dirty = False

        self.width = self.current_state["width"]
        self.height = self.current_state["height"]
        if self.specifies('name'):
            self.name = spec["name"]
        else:
            self.name = "Unknown"
        if self.specifies("height") and self.specifies("width"):
            self.canvas = Canvas(spec["width"],
                            spec["height"])
            self.canvas.set_color_ansi(caca.COLOR_WHITE, caca.COLOR_BLACK)
        else:
            self.canvas = Canvas(0, 0)
            self.canvas.set_color_ansi(caca.COLOR_WHITE, caca.COLOR_BLACK)

        logging.debug("Spec for widget:")
        logging.debug(str(self.spec))

        self.build_all()
