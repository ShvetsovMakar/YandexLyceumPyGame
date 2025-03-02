import pygame
import json

from Config.Characteristics.Characters import CHARACTERS, CHARACTER_ENHANCEMENT
from Sprites.Player.Weapon import Weapon
from Sprites.Player.Breastplate import Breastplate
from Sprites.Player.Leggings import Leggings
from Sprites.Player.Helmet import Helmet


class Player(pygame.sprite.Sprite):
    def __init__(self, name, sprite_group, size, position):
        super().__init__(sprite_group)

        self.name = name

        self.width = size[0]
        self.height = size[1]

        with open(f"Data/Characters/{self.name}.json", "r") as file:
            data = json.load(file)
            self.level = data["level"]
            self.XP = data["XP"]
            self.gold = data["gold"]
            self.skin = data["skin"]

            self.damage = CHARACTERS[self.skin]["damage"] * CHARACTER_ENHANCEMENT ** self.level
            self.health = CHARACTERS[self.skin]["health"] * CHARACTER_ENHANCEMENT ** self.level
            self.agility = CHARACTERS[self.skin]["agility"]

            # Setting up player's body parts images

            self.head_image = pygame.transform.scale(pygame.image.load(f"Graphics/Characters/Heads/{data['skin']}.png"),
                                                     (self.width, self.height))

            self.rect = self.head_image.get_rect()
            self.rect.x = position[0]
            self.rect.y = position[1]

            self.torso_image = pygame.transform.scale(pygame.image.load(f"Graphics/Characters/Torsos/{data['skin']}.png"),
                                                     (self.width, self.height))

            self.legs_image = pygame.transform.scale(pygame.image.load(f"Graphics/Characters/Legs/{data['skin']}.png"),
                                                     (self.width, self.height))

            # Setting up player's gear
            self.gear_sprites = pygame.sprite.Group()

            if data['gear']['weapon']['type'] is None:
                self.weapon = None
            else:
                self.weapon = Weapon(data['gear']['weapon']['type'],
                                     data['gear']['weapon']['level'],
                                     self.gear_sprites,
                                     (self.width, self.height),
                                     (self.rect.x, self.rect.y))

            if data['gear']['armor']['breastplate']['type'] is None:
                self.breastplate = None
            else:
                self.breastplate = Breastplate(data['gear']['armor']['breastplate']['type'],
                                               data['gear']['armor']['breastplate']['level'],
                                               self.gear_sprites,
                                               (self.width, self.height),
                                               (self.rect.x, self.rect.y))

            if data['gear']['armor']['leggings']['type'] is None:
                self.leggings = None
            else:
                self.leggings = Leggings(data['gear']['armor']['leggings']['type'],
                                         data['gear']['armor']['leggings']['level'],
                                         self.gear_sprites,
                                         (self.width, self.height),
                                         (self.rect.x, self.rect.y))

            if data['gear']['armor']['helmet']['type'] is None:
                self.helmet = None
            else:
                self.helmet = Helmet(data['gear']['armor']['helmet']['type'],
                                     data['gear']['armor']['helmet']['level'],
                                     self.gear_sprites,
                                     (self.width, self.height),
                                     (self.rect.x, self.rect.y))

            # Setting up player's inventory

    def draw(self, screen):
        if self.weapon is not None:
            self.weapon.draw(screen)

        if self.breastplate is None:
            screen.blit(self.torso_image, self.rect)
        else:
            self.breastplate.draw(screen)

        if self.leggings is None:
            screen.blit(self.legs_image, self.rect)
        else:
            self.leggings.draw(screen)

        if self.helmet is None:
            screen.blit(self.head_image, self.rect)
        else:
            self.helmet.draw(screen)

    def save(self):
        character_data = {"name": self.name,
                          "skin": self.skin,
                          "level": self.level,
                          "XP": self.XP,
                          "gear": {
                              "weapon": {
                                  "type": None,
                                  "level": None
                              },
                              "armor": {
                                  "helmet": {
                                      "type": None,
                                      "level": None
                                  },
                                  "breastplate": {
                                      "type": None,
                                      "level": None
                                  },
                                  "leggings": {
                                      "type": None,
                                      "level": None
                                  }
                              }
                          },
                          "gold": self.gold,
                          "inventory": []
                          }

        if self.weapon is not None:
            character_data["gear"]["weapon"] = {"type": self.weapon.type,
                                                "level": self.weapon.level}

        if self.helmet is not None:
            character_data["gear"]["armor"]["helmet"] = {"type": self.helmet.type,
                                                         "level": self.helmet.level}

        if self.breastplate is not None:
            character_data["gear"]["armor"]["breastplate"] = {"type": self.breastplate.type,
                                                              "level": self.breastplate.level}

        if self.leggings is not None:
            character_data["gear"]["armor"]["leggings"] = {"type": self.leggings.type,
                                                           "level": self.leggings.level}

        with open(f"Data/Characters/{self.name}.json", "w") as file:
            json.dump(character_data, file, indent=4)

        with open("Data/CurrentCharacter/player.json", "w") as file:
            json.dump(character_data, file, indent=4)