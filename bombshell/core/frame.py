from dataclasses import dataclass

from game.player.character import Character
from game.target import Target
from image.screen import Screen


@dataclass
class Frame:
    character: Character
    target: Target
    screen: Screen = None
