from core.data import ExtractedData
from game.character import Character


class StateHandler:

    def __init__(self):
        self.character = Character()

    def update(self, data: ExtractedData):
        self.character.hp = data.player_health

