import pygame

from Sprites.Mobs.Mob import Mob


class Merchant(Mob):
    def __init__(self, image_path, position, size, sprite_group):
        super().__init__(image_path, position, size, sprite_group)

    def on_click(self):
        pass
