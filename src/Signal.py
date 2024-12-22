class Signal:
    """
    A class of a signal. It allows to announce that an event happened
    and connect responses (functions that will be run afterward).
    """
    def __init__(self) -> None:
        self.slots = []

    def addSlot(self, func) -> None:
        """
        Adds a response to an event.
        :param func: func to be run as a response to an event.
        """
        self.slots.append(func)


    def emit(self, *args: any, **kwds: any) -> None:
        """
        Announces that an event occurred. Runs all the functions connected to it.
        :param args: arguments that will be passed to the functions.
        :param kwds: keyword arguments that will be passed to the functions.
        """
        for slot in self.slots:
            slot(*args, **kwds)
