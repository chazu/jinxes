import logging
logging.basicConfig(level=logging.DEBUG)

from widget import Widget
from app import App

import hooks

app = App('tui.json')

# Focused widget (should be part of app init)
app.focused_widget = app.display.widgets[0]

app.run()
