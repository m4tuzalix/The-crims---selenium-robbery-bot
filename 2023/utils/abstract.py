from typing import Protocol


class Action(Protocol):
    def do_action(self):
        pass

    def restore(self):
        pass
