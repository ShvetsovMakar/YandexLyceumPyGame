import pygame
import sys

from OnClickFunctions import on_click_main_menu_functions

from Sprites.Button import Button
from Sprites.Label import Label


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
                             on_click_main_menu_functions.exit_button)

        add_character_button = Button('Graphics/main_menu/add_character_button/basic.png',
                                      'Graphics/main_menu/add_character_button/hovered_on.png',
                                      (self.width // 2 - width // 2,
                                       self.height // 4 * 3 - height // 2 - height - height // 5),
                                      (width, height),
                                      buttons,
                                      on_click_main_menu_functions.add_character_button)

        play_button = Button('Graphics/main_menu/play_button/basic.png',
                             'Graphics/main_menu/play_button/hovered_on.png',
                             (self.width // 2 - width // 2,
                              self.height // 4 * 3 - height // 2 - 2 * (height + height // 5)),
                             (width, height),
                             buttons,
                             on_click_main_menu_functions.play_button)

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
        pass

    def play(self):
        pass


# Initializing pygame and game constants
pygame.init()
FPS = 90

# Starting game
game = Game()
game.main_menu()
