from dataclasses import dataclass

from game.player.character import Character
from game.target import Target
from image.screeninterceptor import ScreenInterceptor


@dataclass
class Frame:
    character: Character
    target: Target
    screen: ScreenInterceptor = None
