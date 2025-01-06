import pygame
import sys

from OnClickFunctions import on_click_main_menu, on_click_add_character

from Sprites.Button import Button
from Sprites.Label import Label
from Sprites.TextBox import TextBox
from Sprites.InputBox import InputBox


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.width = self.screen.get_size()[0]
        self.height = self.screen.get_size()[1]

    def main_menu(self):
        # Initializing buttons
        buttons = pygame.sprite.Group()

        width = self.width // 2
        height = self.height // 8

        exit_button = Button('Graphics/main_menu/exit_button/basic.png',
                             'Graphics/main_menu/exit_button/hovered_on.png',
                             (self.width // 2 - width // 2,
                              self.height // 4 * 3 - height // 2),
                             (width, height),
                             buttons,
                             on_click_main_menu.exit)

        add_character_button = Button('Graphics/main_menu/add_character_button/basic.png',
                                      'Graphics/main_menu/add_character_button/hovered_on.png',
                                      (self.width // 2 - width // 2,
                                       self.height // 4 * 3 - height // 2 - height - height // 5),
                                      (width, height),
                                      buttons,
                                      on_click_main_menu.add_character)

        play_button = Button('Graphics/main_menu/play_button/basic.png',
                             'Graphics/main_menu/play_button/hovered_on.png',
                             (self.width // 2 - width // 2,
                              self.height // 4 * 3 - height // 2 - 2 * (height + height // 5)),
                             (width, height),
                             buttons,
                             on_click_main_menu.play)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/main_menu/background/basic.png',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        # Main menu loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            button.on_click(self)

            # Updating buttons' images
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.set_hovered_on_image()
                else:
                    button.set_basic_image()

            # Updating screen
            self.screen.fill((0, 0, 0))

            labels.draw(self.screen)
            buttons.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def add_character(self):
        # Initializing buttons
        buttons = pygame.sprite.Group()

        width = self.width // 20
        height = self.height // 5

        forward_button = Button('Graphics/add_character/forward_button/basic.png',
                                'Graphics/add_character/forward_button/hovered_on.png',
                                (self.width // 2 + self.width // 5 - width // 2,
                                 self.height // 2 - height // 2),
                                (width, height),
                                buttons,
                                on_click_add_character.forward)

        backward_button = Button('Graphics/add_character/backward_button/basic.png',
                                 'Graphics/add_character/backward_button/hovered_on.png',
                                 (self.width // 2 - self.width // 5 - width // 2,
                                  self.height // 2 - height // 2),
                                 (width, height),
                                 buttons,
                                 on_click_add_character.backward)

        width = self.width // 4
        height = self.height // 10

        to_main_menu_button = Button('Graphics/add_character/to_main_menu_button/basic.png',
                                     'Graphics/add_character/to_main_menu_button/hovered_on.png',
                                     (self.width // 2 - width - width // 50,
                                      self.height // 10 * 9 - height),
                                     (width, height),
                                     buttons,
                                     on_click_add_character.to_main_menu)

        create_character_button = Button('Graphics/add_character/create_character_button/basic.png',
                                         'Graphics/add_character/create_character_button/hovered_on.png',
                                         (self.width // 2 + width // 50,
                                          self.height // 10 * 9 - height),
                                         (width, height),
                                         buttons,
                                         on_click_add_character.create_character)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/add_character/background/basic.png',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        character_images_paths = ["Graphics/characters/Guts.png",
                                  "Graphics/characters/Witcher.png",
                                  "Graphics/characters/Kratos.png",
                                  "Graphics/characters/Griffith.png"]

        width = self.height // 2
        height = self.height // 2

        character = Label(character_images_paths[0],
                          (self.width // 2 - width // 2, self.height // 2 - height // 2),
                          (width, height),
                          labels)

        # Initializing text boxes
        text_boxes = []

        character_names = ["Guts",
                           "Witcher",
                           "Kratos",
                           "Griffith"]

        character_name = TextBox(character_names[0],
                                 pygame.font.Font("Fonts/Norse/basic.otf", self.width // 40),
                                 (self.width // 2, self.height // 2 - self.height // 4 - self.width // 40),
                                 (0, 0, 0),
                                 None,
                                 None)
        text_boxes.append(character_name)

        # Initializing character index in lists of names and images paths
        character_index = 0

        # Add character loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            if button.on_click(self, character_index)[0]:
                                return
                            else:
                                character_index = button.on_click(self, character_index)[1]
                                character.change_image(character_images_paths[character_index])
                                character_name.change_text(character_names[character_index])

            # Updating buttons' images
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.set_hovered_on_image()
                else:
                    button.set_basic_image()

            # Updating screen
            self.screen.fill((0, 0, 0))

            labels.draw(self.screen)
            buttons.draw(self.screen)
            for text_box in text_boxes:
                text_box.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def play(self):
        pass


# Initializing pygame and game constants
pygame.init()
FPS = 90

# Starting game
game = Game()
game.main_menu()
