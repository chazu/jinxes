from widget import Widget

class FileParser:

    def __init__(self):
        pass

    def parse(self, widgets):
        acc = []
        for widget in widgets:
            acc.append(Widget(widget))
        return acc
