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

class Widget(object):

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
            self.canvas.draw_box(0, 0, self.spec["width"],
                                 self.spec["height"],"X")

    def draw(self):
        if self.border:
            self.draw_border()
        self.draw_text_buffer()

    def specifies(self, key, value=None):
        """
        True if the spec doc has the key.
        If value is passed in, True only
        if key is present and equal to value
        """
        return key in self.spec.keys() and (
            self.spec[key] == value if value != None else True)

    def border_builder(self):
        if self.specifies("border", True):
            print "drawing border"
            self.border = True

    def set_anchor(self):
        if self.specifies("anchor"):
            self.anchor = self.spec["anchor"]
        else:
            self.anchor = (0, 0)

    def text_buffer_builder(self):
        if self.specifies("text"):
            self.text_buffer = self.spec["text"]
        if self.specifies("border", True):
            self.text_origin = [1, 1]
        else:
            self.text_origin = (0, 0)

    def __init__(self, spec):
        self.spec = spec
        self.width = self.spec["width"]
        self.height = self.spec["height"]
        if self.specifies('name'):
            self.name = spec["name"]
        else:
            self.name = "Unknown"
        if self.specifies("height") and self.specifies("width"):
            print "creating canvas of specified size"
            self.canvas = Canvas(spec["width"],
                            spec["height"])
            self.canvas.set_color_ansi(caca.COLOR_WHITE, caca.COLOR_BLACK)
        else:
            print "creating generic size canvas"
            self.canvas = Canvas(0, 0)
            self.canvas.set_color_ansi(caca.COLOR_WHITE, caca.COLOR_BLACK)
        self.set_anchor()
        self.border_builder()
        self.text_buffer_builder()
