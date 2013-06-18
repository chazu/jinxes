import caca
from caca.canvas import Canvas, CanvasError
from caca.display import Display, DisplayError, Event

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
        if path != None and isDict(
                multiIndex(self.spec, path)
        ):
            try:
                target = multiIndex(self.spec, path)
            except KeyError:
                print "WARNING: Key error when requesting path " + \
                    str(path) + " for widget " + self.name
                target = self.spec
        else:
            target = self.spec
        return key in target.keys() and (
            target[key] == value if value != None else True)

    def specifies_not_equal(self, key, value):
        """
        True if the value is specified but not equal to given value
        """
        return self.spec[key] != value

    def draw_text_buffer(self):
        draw_width = (self.width - 2 if self.border == True else self.width)
        text_lines = chunks(self.text_buffer, draw_width)
        print "Text lines: " + str(text_lines)
        line_start = self.text_origin
        for line in text_lines:
            self.canvas.put_str(line_start[0],
                                line_start[1],
                                line)
            line_start[1] += 1

    def draw_border(self):
        if self.border["visible"] and self.border["present"]:
            print "INFO: Border char: " + str(self.border["character"])
            char = self.border["character"]
            self.canvas.draw_box(0, 0, self.spec["width"],
                                 self.spec["height"],str(char))

    def draw(self):
        if self.border:
            self.draw_border()
        self.draw_text_buffer()

    def border_builder(self):
        if self.specifies("border") and isDict(self.spec["border"]):
            print("DEBUG: Parsing border spec: ")
            print(str(self.spec["border"]))
            print("INFO:  Overriding default border attrs")
            self.border = Widget.defaultBorderAttributes.copy()
            self.border.update(self.spec["border"])
        else:
            print("INFO:  Using default border attrs")
            self.border = Widget.defaultBorderAttributes.copy()

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

    def __init__(self, spec):
        self.spec = spec
        self.width = self.spec["width"]
        self.height = self.spec["height"]
        if self.specifies('name'):
            self.name = spec["name"]
        else:
            self.name = "Unknown"
        print("INFO: Creating widget " + self.spec["name"])
        if self.specifies("height") and self.specifies("width"):
            print("DEBUG: creating canvas of specified size")
            self.canvas = Canvas(spec["width"],
                            spec["height"])
            self.canvas.set_color_ansi(caca.COLOR_WHITE, caca.COLOR_BLACK)
        else:
            print "creating generic size canvas"
            self.canvas = Canvas(0, 0)
            self.canvas.set_color_ansi(caca.COLOR_WHITE, caca.COLOR_BLACK)
        self.anchor_builder()
        self.border_builder()
        self.text_buffer_builder()
