class LocalEventDispatch:
    """
    Takes oapplication-level events and routes them to the app's local message
    queue.

    TODO: Since both this class and TartanDisplay use
    the spec, pass it into both constructors
    """

    def __init__(self, app):
        self.app = app
        self.messages = []

    def emit_message(self, message):
        """
        """
        self.messages.append(message)
