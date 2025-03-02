import pygame
import random

from Sprites.Mobs.Mob import Mob

from Config.Characteristics.Helmets import HELMETS
from Config.Characteristics.Breastplates import BREASTPLATES
from Config.Characteristics.Leggings import LEGGINGS
from Config.Characteristics.Weapons import WEAPONS, WEAPON_ENHANCEMENT

from Sprites.Player.Helmet import Helmet
from Sprites.Player.Breastplate import Breastplate
from Sprites.Player.Leggings import Leggings
from Sprites.Player.Weapon import Weapon

class Merchant(Mob):
    def __init__(self, image_path, position, size, sprite_group):
        super().__init__(image_path, position, size, sprite_group)

    def on_click(self, player):
        if player.gold < 50:
            return

        helmets = list(HELMETS.keys())
        breastplates = list(BREASTPLATES.keys())
        leggings = list(LEGGINGS.keys())
        weapons = list(WEAPONS.keys())

        gear_elements = ["Helmet", "Breastplate", "Leggings", "Weapon"]
        gear_element = random.choice(gear_elements)

        if gear_element == "Helmet":
            gear_element = random.choice(helmets)
            player.helmet = Helmet(gear_element,
                                   player.level,
                                   player.gear_sprites,
                                   (player.width, player.height),
                                   (player.rect.x, player.rect.y))

        if gear_element == "Breastplate":
            gear_element = random.choice(breastplates)
            player.breastplate = Breastplate(gear_element,
                                             player.level,
                                             player.gear_sprites,
                                             (player.width, player.height),
                                             (player.rect.x, player.rect.y))

        if gear_element == "Leggings":
            gear_element = random.choice(leggings)
            player.leggings = Leggings(gear_element,
                                       player.level,
                                       player.gear_sprites,
                                       (player.width, player.height),
                                       (player.rect.x, player.rect.y))

        if gear_element == "Weapon":
            gear_element = random.choice(weapons)
            player.weapon = Weapon(gear_element,
                                   player.level,
                                   player.gear_sprites,
                                   (player.width, player.height),
                                   (player.rect.x, player.rect.y))

        player.gold -= 50
        player.save()

