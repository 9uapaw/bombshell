from game.control.control import CharacterController
from game.position.position import Position


class StuckPolicy:
    HISTORY_LIMIT = 10

    def __init__(self, controller: CharacterController):
        self.controller = controller
        self._coords = []
        self._current = 0

    def add(self, position: Position):
        if self._current == self.HISTORY_LIMIT:
            self._current = 0

        if len(self._coords) < self.HISTORY_LIMIT:
            self._coords.append(position)
        else:
            self._coords.insert(self._current, position)

        self._current += 1