from widget import Widget

class FileParser:

    def __init__(self, app):
        self.app = app
        pass

    def parse(self, widgets):
        acc = []
        for widget in widgets:
            acc.append(Widget(self.app, widget))
        return acc
