import pygame

from Config.Characteristics.Weapons import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, level, sprite_group, size, position):
        super().__init__(sprite_group)

        self.type = name

        # Setting up weapon image
        self.width = size[0]
        self.height = size[1]

        image = pygame.image.load(f"Graphics/Characters/Weapons/{self.type}.png")
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # Setting up weapon characteristics
        data = WEAPONS[self.type]

        self.level = level
        self.damage = data["damage"] * WEAPON_ENHANCEMENT ** self.level
        self.hits = data["hits"]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
