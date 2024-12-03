class Signal:
    def __init__(self) -> None:
        self.slots = []

    def addSlot(self, func) -> None:
        self.slots.append(func)


    def emit(self, *args: any, **kwds: any) -> any:
        for slot in self.slots:
            slot(*args, **kwds)
