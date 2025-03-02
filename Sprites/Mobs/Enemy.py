import pygame

from Sprites.Mobs.Mob import Mob


class Enemy(Mob):
    def __init__(self, image_path, position, size, sprite_group, damage, health):
        super().__init__(image_path, position, size, sprite_group)

        self.damage = damage
        self.health = health

    def on_click(self, player):
        pass
