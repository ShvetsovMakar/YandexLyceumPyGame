import pygame

from Sprites.Mobs.Mob import Mob


class Warrior(Mob):
    def __init__(self, image_path, position, size, sprite_group):
        super().__init__(image_path, position, size, sprite_group)

    def on_click(self, player):
        return "forest"
