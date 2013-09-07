import logging
logging.basicConfig(level=logging.DEBUG)

from widget import Widget
from app import App

import hooks

app = App("login.json")

app.run()
