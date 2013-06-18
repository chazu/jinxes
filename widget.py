import time
from copy import copy

import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

def listify(gen):
    "Convert a generator into a function which returns a list"
    def patched(*args, **kwargs):
        return list(gen(*args, **kwargs))
    return patched

@listify
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def multiIndex(the_object, index_array):
    """
    TODO Write this docstring
    """
    return reduce(lambda obj, key: obj[key], index_array, the_object)

def isDict(thing):
    return type(thing) == dict


class Widget(object):

    # Default json structures for nested instance config info
    # Note that simple base-level data will just be stored in
    # instance attributes without default attr dicts to override

    defaultBorderAttributes = {
        "present": True,
        "visible": True,
        "character": "X",
        "fgColor": 0,
        "bgColor": 1
        }

    defaultScrollingAttributes = {
        "scroll": False,
        "currentLine": 0
        }

    def specifies(self, key, value=None, path=None):
        """
        Key - The key to search for
        Value - A value to check equality for
        Path - The path in the spec to search

        True if the spec doc has the key.
        If value is passed in, True only
        if key is present and equal to value
        """
        try:
            if path != None and isDict(multiIndex(self.spec, path)):
                target = multiIndex(self.spec, path)
            else:
                target = self.spec
                return key in target.keys() and (
                    target[key] == value if value != None else True)
        except KeyError:
            print "WARNING: Key error when requesting path " + \
                str(path) + " for widget " + self.name
            target = self.spec

    def specifies_not_equal(self, key, value):
        """
        True if the value is specified but not equal to given value
        """
        return self.spec[key] != value

    def draw_line_buffer(self):
        for line in self.get_visible_slice():
            self.canvas.put_str(line_start[0],
                                line_start[1],
                                line)
            line_start[1] += 1

    def draw_border(self):
        if self.border["visible"] and self.border["present"]:
            char = self.border["character"]
            self.canvas.draw_box(0, 0, self.spec["width"],
                                 self.spec["height"],str(char))

    def draw(self):
        self.canvas.clear()
        self.draw_line_buffer()
        self.draw_border()

    # Builder methods - take the spec for the widget and build out
    # instance state

    def border_builder(self):
        if self.specifies("border") and isDict(self.spec["border"]):
            print(str(self.spec["border"]))
            self.border = Widget.defaultBorderAttributes.copy()
            self.border.update(self.spec["border"])
        else:
            self.border = Widget.defaultBorderAttributes.copy()

    def line_buffer_builder(self):
        """
        Update internal line buffer based on dimensions
        of widget, border and length of text contents

        Call this after resize
        """
        draw_width = (self.width - 2 if self.border["present"] == True else self.width)
        self.line_buffer = chunks(self.text_buffer, draw_width)

    def text_buffer_builder(self):
        if self.specifies("text"):
            self.text_buffer = self.spec["text"]
        if self.border["present"]:
            self.text_origin = [1, 1]
        else:
            self.text_origin = [0, 0]

    def anchor_builder(self):
        if self.specifies("anchor"):
            self.anchor = self.spec["anchor"]
        else:
            self.anchor = (0, 0)

    def visible_slice_builder(self):
        """
        initialize or change visible slice
        """
        if self.border["present"]:
            self.visible_lines = self.height - 2
        else:
            self.visible_lines = self.height

    def scroll_builder(self):
        """
        Build/Initialize state related to scrolling capabilities and
        behavior
        """
        # set up scrolling
        if self.specifies("scroll"):
            self.scroll = Widget.defaultScrollingAttributes.copy()
            self.scroll.update(self.spec["scroll"])
        else:
            self.scroll = Widget.defaultScrollingAttributes.copy()

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
        # res = self.line_buffer[self.scroll["currentLine"]:
        #                                     self.scroll["currentLine"] + \
        #                                         self.visible_lines]
        print str(res)
        return res

    def __init__(self, spec):
        self.spec = spec
        self.width = self.spec["width"]
        self.height = self.spec["height"]
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
        self.anchor_builder()
        self.border_builder()
        self.scroll_builder()
        self.text_buffer_builder()
        self.line_buffer_builder()
        self.visible_slice_builder()
