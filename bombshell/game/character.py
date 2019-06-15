import enum


class Resource(enum.Enum):
    mana = 0
    energy = 1
    rage = 2


class Character:

    def __init__(self, resource_type: Resource):
        self.hp = 0
        self.resource = 0
        self.position = (0, 0)
        self.resource_type = resource_type
        self.is_moving = False

    def update_health(self, health: int):
        self.hp = health

    def __repr__(self):
        return "<HP: {}, Position: {}, Resource: {} {}>".format(self.hp, self.position, self.resource, self.resource_type.name)
