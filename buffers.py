from util import chunks, isDict

class AbstractBuffer:

    defaultScrollingAttributes = {
        "scroll": True,
        "currentLine": 0,
        "noVisibleLines": 0
        }


class TextualBuffer(AbstractBuffer):

    def __init__(self, widget, text=None):
        self.widget = widget
        self.draw_width = 0

        self.scroll = TextualBuffer.defaultScrollingAttributes.copy()
        if self.widget.specifies("scroll") and \
           isDict(self.widget.current_state["scroll"]):
                  self.scroll.update(self.widget.current_state["scroll"])

        self._text = text if text != None else ""
        self._lines = []
        self.build()

    def __getitem__(self, index):
            return self._lines[index]

    def get_text(self):
        return self._text

    def add_text(self, text):
        self._text += text
        print "Text: " + self._text

    def clear(self):
        self._lines = []
        self._text = ""

    def build(self):
        # set draw width
        self.draw_width = (self.widget.current_state["width"] - 2
                           if self.widget.specifies("border")
                           else self.widget.width)
        self.build_lines()
        self.build_scroll_characteristics()

    def build_lines(self):
        self._lines = chunks(self._text, self.draw_width)
        self.widget.scroll["maxCurrentLine"] = len(self._lines)

    def build_scroll_characteristics(self):
        if self.widget.specifies("border"):
            self.scroll["noVisibleLines"] = \
                                self.widget.current_state["height"] - 2
        else:
            self.scroll["noVisibleLines"] = self.widget.current_state["height"]

    def get_visible_slice(self):
        print self.scroll
        start = self.scroll["currentLine"]
        end = start + self.scroll["noVisibleLines"]
        res = self._lines[start:]
        res = res[:end]
        return res


class LineBuffer:

    
