from dataclasses import dataclass

from PIL.Image import Image

from game.player.character import Character
from game.target import Target


@dataclass
class Frame:
    character: Character
    target: Target
    screen: Image = None
