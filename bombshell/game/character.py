import enum


class Resource(enum.Enum):
    mana = 0
    energy = 1
    rage = 2


class Character:

    def __init__(self):
        self.hp = 0
        self.resource = 0
        self.resource_type = None
        self.controller = None
        self.position = (0, 0)

    def update_health(self, health: int):
        self.hp = health

    def __repr__(self):
        return "<HP: {}>".format(self.hp)
