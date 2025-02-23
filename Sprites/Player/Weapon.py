import pygame

from Config.Characteristics.Weapons import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, level, sprite_group, size, position):
        super().__init__(sprite_group)

        self.name = name

        self.width = size[0]
        self.height = size[1]

        image = pygame.image.load(f"Graphics/Characters/Weapons/{name}.png")
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        data = WEAPONS[name]

        self.level = level
        self.damage = data[0] * WEAPON_ENHANCEMENT ** self.level
