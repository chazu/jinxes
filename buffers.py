from util import chunks, isDict
import logging

class AbstractBuffer(object):

    defaultScrollingAttributes = {
        "scroll": True,
        "currentLine": 0,
        "noVisibleLines": 0
        }

    def __init__(self, widget, text=None):
        self.widget = widget
        self.draw_width = 0

        self.scroll = TextualBuffer.defaultScrollingAttributes.copy()

    def get_visible_slice(self):
        raise Exception, "must be implemented by subclass of AbstractBuffer"

    def build(self):
        raise Exception, "must be implemented by subclass of AbstractBuffer"

    def __getitem__(self, index):
        raise Exception, "must be implemented by subclass of AbstractBuffer"

    def clear(self):
        raise Exception, "must be implemented by subclass of AbstractBuffer"


class TextualBuffer(AbstractBuffer):

    def __init__(self, widget, text=None):
        super(TextualBuffer, self).__init__(widget, text)

        if self.widget.specifies("scroll") and \
           isDict(self.widget.current_state["scroll"]):
                  self.scroll.update(self.widget.current_state["scroll"])

        self._text = self.widget.current_state["contents"]['text'] \
            if self.widget.specifies('text',
                                     path=['contents']) else ""
        self._lines = []
        self.build()

    def __getitem__(self, index):
            return self._lines[index]

    def get_text(self):
        return self._text

    def add_text(self, text):
        self._text += text

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
        self.scroll["maxCurrentLine"] = len(self._lines)

    def build_scroll_characteristics(self):
        if self.widget.specifies("border"):
            self.scroll["noVisibleLines"] = \
                                self.widget.current_state["height"] - 2
        else:
            self.scroll["noVisibleLines"] = self.widget.current_state["height"]

    def get_visible_slice(self):
        start = self.scroll["currentLine"]
        end = start + self.scroll["noVisibleLines"]
        res = self._lines[start:]
        res = res[:end]
        return res


class LineBuffer(TextualBuffer):

    def __init__(self, widget, text=None):
        super(LineBuffer, self).__init__(widget, text)
        self.point = [0,0]
        self._lines = [""]

        logging.debug(self._lines)

    def build_lines(self):
        self.scroll["maxCurrentLine"] = len(self._lines)

    def clear(self):
        self._lines = [""]

    def point_to_next_line(self):
        self.point[0] += 1
        self.point[1] == 0
        while len(self._lines) < self.point[0] + 1:
            self._lines.append("")

    def point_to_last_line(self):
        self.point[0] = len(self._lines) - 1

    def last_line(self):
        return self._lines[-1]

    def point_to_end_of_buffer(self):
        self.point[0] = len(self._lines)
        self.point[1] = len(self._lines[-1])

    def point_to_end_of_line(self):
        self.point[1] = len(self._lines[-1]) - 1

    def adjust_point_by_lines(self, number):
        self.point[0] += number

    def adjust_point_by_columns(self, number):
        self.point[1] += number

    def get_text(self):
        return "".join(self._lines)

    def add_text(self, text):
        if len(text) + len(self._lines[self.point[0]]) > self.draw_width:
            self.point_to_next_line()
        if len(text) > self.draw_width:
            lines_to_add = chunks(text, self.draw_width)
            lines_to_advance = len(lines_to_add)
            for line in lines_to_add:
                self._lines.append(line)
            self.adjust_point_by_lines(lines_to_advance)
        else:
            self._lines[self.point[0]] += text
        self.point_to_end_of_line()
