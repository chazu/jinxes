class LocalEventDispatch:
    """
    Takes events from inside of the engine (caca events
    such as keypresses), matches them to widgets
    and executes callbacks which affect widgets.

    Mapping of events to widgets is established at
    instance initialization based on the specification
    document used to construct the UI.
    TODO: Since both this class and TartanDisplay use
    the spec, pass it into both constructors
    """

    def __init__(self):
        """
        Parse the spec and create mappings to various
        functions that will affect UI state
        """
        pass

    def dispatch_events(self, events):
        """
        Do your magic: tell widgets what to do
        """
        pass
