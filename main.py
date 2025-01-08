import pygame
import sys

from Config.constants import *

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

        exit_button = Button('Graphics/MainMenu/ExitButton/basic.png',
                             'Graphics/MainMenu/ExitButton/hovered_on.png',
                             (self.width // 2 - width // 2,
                              self.height // 4 * 3 - height // 2),
                             (width, height),
                             buttons,
                             on_click_main_menu.exit)

        add_character_button = Button('Graphics/MainMenu/AddCharacterButton/basic.png',
                                      'Graphics/MainMenu/AddCharacterButton/hovered_on.png',
                                      (self.width // 2 - width // 2,
                                       self.height // 4 * 3 - height // 2 - height - height // 5),
                                      (width, height),
                                      buttons,
                                      on_click_main_menu.add_character)

        play_button = Button('Graphics/MainMenu/PlayButton/basic.png',
                             'Graphics/MainMenu/PlayButton/hovered_on.png',
                             (self.width // 2 - width // 2,
                              self.height // 4 * 3 - height // 2 - 2 * (height + height // 5)),
                             (width, height),
                             buttons,
                             on_click_main_menu.play)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/MainMenu/Background/basic.png',
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

        forward_button = Button('Graphics/AddCharacter/ForwardButton/basic.png',
                                'Graphics/AddCharacter/ForwardButton/hovered_on.png',
                                (self.width // 2 + self.width // 5 - width // 2,
                                 self.height // 2 - height // 2),
                                (width, height),
                                buttons,
                                on_click_add_character.forward)

        backward_button = Button('Graphics/AddCharacter/BackwardButton/basic.png',
                                 'Graphics/AddCharacter/BackwardButton/hovered_on.png',
                                 (self.width // 2 - self.width // 5 - width // 2,
                                  self.height // 2 - height // 2),
                                 (width, height),
                                 buttons,
                                 on_click_add_character.backward)

        width = self.width // 4
        height = self.height // 10

        to_main_menu_button = Button('Graphics/AddCharacter/ToMainMenuButton/basic.png',
                                     'Graphics/AddCharacter/ToMainMenuButton/hovered_on.png',
                                     (self.width // 2 - width - width // 50,
                                      self.height // 10 * 9 - height),
                                     (width, height),
                                     buttons,
                                     on_click_add_character.to_main_menu)

        create_character_button = Button('Graphics/AddCharacter/CreateCharacterButton/basic.png',
                                         'Graphics/AddCharacter/CreateCharacterButton/hovered_on.png',
                                         (self.width // 2 + width // 50,
                                          self.height // 10 * 9 - height),
                                         (width, height),
                                         buttons,
                                         on_click_add_character.create_character)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/AddCharacter/Background/basic.png',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        character_images_paths = ["Graphics/Characters/Guts.png",
                                  "Graphics/Characters/Witcher.png",
                                  "Graphics/Characters/Kratos.png",
                                  "Graphics/Characters/Griffith.png"]

        width = self.height // 2
        height = self.height // 2

        character = Label(character_images_paths[0],
                          (self.width // 2 - width // 2, self.height // 2 - height // 2),
                          (width, height),
                          labels)

        # Initializing text boxes
        text_boxes = []

        character_name = TextBox(CHARACTER_NAMES[0],
                                 pygame.font.Font("Fonts/Norse/bold.otf", self.width // 40),
                                 (self.width // 2, self.height // 2 - self.height // 4 - self.width // 40),
                                 (0, 0, 0),
                                 None,
                                 None)
        text_boxes.append(character_name)

        # Initializing input boxes
        input_boxes = []

        input_name = InputBox("",
                              pygame.font.Font("Fonts/Norse/basic.otf", self.width // 40),
                              (self.width // 3, self.width // 32),
                              (self.width // 3, self.height // 20),
                              MAX_NAME_LENGTH,
                              (0, 0, 0),
                              (255, 255, 255),
                              (200, 200, 200),
                              (0, 0, 0))
        input_boxes.append(input_name)

        # Initializing character index in lists of names and images paths
        character_index = 0

        # Add character loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    for button in buttons:
                        if not button.rect.collidepoint(pygame.mouse.get_pos()):
                            continue

                        if button.on_click(self, character_index, input_name.text.lower())[0]:
                            return
                        else:
                            character_index = button.on_click(self, character_index, input_name.text.lower())[1]

                            character.change_image(character_images_paths[character_index])
                            character_name.change_text(CHARACTER_NAMES[character_index])
                        break

                    for input_box in input_boxes:
                        input_box.active = (input_box.x <= x <= input_box.x + input_box.width and
                                            input_box.y <= y <= input_box.y + input_box.height)

                if event.type == pygame.KEYDOWN:
                    for input_box in input_boxes:
                        if not input_box.active:
                            continue

                        if event.key == pygame.K_RETURN:
                            input_box.active = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_box.text = input_box.text[:-1]
                        elif len(input_box.text) < input_box.max_length:
                            input_box.text += event.unicode
                        break

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
            for input_box in input_boxes:
                input_box.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def play(self):
        pass


# Initializing all pygame modules
pygame.init()

# Starting game
game = Game()
game.main_menu()
