import pygame
import sys
import os
import json

from Config.constants import *

from OnClickFunctions import (on_click_main_menu, on_click_add_character, on_click_choose_character,
                              on_click_to_main_menu)

from Sprites.Button import Button
from Sprites.Label import Label
from Sprites.TextBox import TextBox
from Sprites.InputBox import InputBox

from Sprites.Tile import Tile

from Sprites.Player.Player import Player

sys.setrecursionlimit(10 ** 6)


class Camera:
    def __init__(self, screen_size):
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.screen_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.screen_height // 2)


class Map:
    def __init__(self, screen_size, screen, field="Config/Maps/lobby.txt"):
        self.screen = screen

        # Setting up tiles width and height
        self.width = screen_size[0]
        self.height = screen_size[1]

        self.tile_width = self.tile_height = self.height // 10

        # Setting up tiles

        if field == "forest":
            field = self.generate_forest()

        else:
            with open(field, 'r') as fieldFile:
                field = [line.strip() for line in fieldFile]

        self.tiles_group = pygame.sprite.Group()
        self.board = []

        for y in range(len(field)):
            for x in range(len(field[y])):
                self.board.append([])
                if field[y][x] == "G":
                    self.board[-1].append(Tile("Graphics/Tiles/Grass.png",
                                               self.tiles_group,
                                               (x * self.tile_width, y * self.tile_height),
                                               (self.tile_width, self.tile_height),
                                               True))

                if field[y][x] == "S":
                    self.board[-1].append(Tile("Graphics/Tiles/Stone.png",
                                               self.tiles_group,
                                               (x * self.tile_width, y * self.tile_height),
                                               (self.tile_width, self.tile_height),
                                               False))

                if field[y][x] == "T":
                    self.board[-1].append(Tile("Graphics/Tiles/Tree.png",
                                               self.tiles_group,
                                               (x * self.tile_width, y * self.tile_height),
                                               (self.tile_width, self.tile_height),
                                               False))

    def generate_forest(self):
        field = []

        return field

    def render(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.board[y][x].draw(self.screen)

    def get_tile(self, mouse_pos):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].rect.collidepoint(mouse_pos):
                    return self.board[y][x]
        return None

    def on_click(self, mouse_pos, player):
        tile = self.get_tile(mouse_pos)

        if tile is None:
            return [None, None]

        player_pos = [player.rect.x // self.tile_width, player.rect.y // self.tile_height]
        tile_pos = [tile.rect.x // self.tile_width, tile.rect.y // self.tile_height]

        # Checking if player is able to move to this tile
        if -1 <= player_pos[0] - tile_pos[0] <= 1 and -1 <= player_pos[1] - tile_pos[1] <= 1 and tile.walkable:
            return ["move", [tile.rect.x - player.rect.x, tile.rect.y - player.rect.y]]

        return [None, None]


class Game:
    def __init__(self):
        pygame.display.set_caption(GAME_TITLE)
        icon = pygame.image.load("Graphics/Icon/Icon.jpg")
        pygame.display.set_icon(icon)

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

        choose_character_button = Button('Graphics/MainMenu/PlayButton/basic.png',
                                         'Graphics/MainMenu/PlayButton/hovered_on.png',
                                         (self.width // 2 - width // 2,
                                          self.height // 4 * 3 - height // 2 - 2 * (height + height // 5)),
                                         (width, height),
                                         buttons,
                                         on_click_main_menu.play)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/MainMenu/Background/basic.jpg',
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

        background = Label('Graphics/AddCharacter/Background/basic.jpg',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        character_images_paths = ["Graphics/Characters/Characters/Guts.png",
                                  "Graphics/Characters/Characters/Witcher.png",
                                  "Graphics/Characters/Characters/Kratos.png",
                                  "Graphics/Characters/Characters/Griffith.png"]

        width = self.height // 2
        height = self.height // 2

        character = Label(character_images_paths[0],
                          (self.width // 2 - width // 2, self.height // 2 - height // 2),
                          (width, height),
                          labels)

        # Initializing text boxes
        text_boxes = pygame.sprite.Group()

        character_name = TextBox(CHARACTER_NAMES[0],
                                 pygame.font.Font("Fonts/Norse/bold.otf", self.width // 40),
                                 (self.width // 2, self.height // 2 - self.height // 4 - self.width // 40),
                                 text_boxes,
                                 (0, 0, 0),
                                 None,
                                 None)

        # Initializing input boxes
        input_boxes = pygame.sprite.Group()

        input_name = InputBox("",
                              pygame.font.Font("Fonts/Norse/basic.otf", self.width // 40),
                              (self.width // 3, self.width // 32),
                              (self.width // 3, self.height // 20),
                              MAX_NAME_LENGTH,
                              input_boxes,
                              (0, 0, 0),
                              (255, 255, 255),
                              (200, 200, 200),
                              (0, 0, 0))

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

                        if button.on_click(character_index, input_name.text.lower())[0]:
                            return
                        else:
                            character_index = button.on_click(character_index, input_name.text.lower())[1]

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
                        elif len(input_box.text) < input_box.max_length and event.unicode not in FORBIDDEN_SYMBOLS:
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

    def choose_character(self):
        # Initializing buttons
        buttons = pygame.sprite.Group()

        width = self.width // 20
        height = self.height // 5

        forward_button = Button('Graphics/ChooseCharacter/ForwardButton/basic.png',
                                'Graphics/ChooseCharacter/ForwardButton/hovered_on.png',
                                (self.width // 2 + self.width // 5 - width // 2,
                                 self.height // 2 - height // 2),
                                (width, height),
                                buttons,
                                on_click_choose_character.forward)

        backward_button = Button('Graphics/ChooseCharacter/BackwardButton/basic.png',
                                 'Graphics/ChooseCharacter/BackwardButton/hovered_on.png',
                                 (self.width // 2 - self.width // 5 - width // 2,
                                  self.height // 2 - height // 2),
                                 (width, height),
                                 buttons,
                                 on_click_choose_character.backward)

        width_ = (self.width // 5 * 2 + width) // 2 - self.width // 100
        height_ = self.height // 10

        to_main_menu_button = Button('Graphics/ChooseCharacter/ToMainMenuButton/basic.png',
                                     'Graphics/ChooseCharacter/ToMainMenuButton/hovered_on.png',
                                     (self.width // 2 - self.width // 5 - width // 2,
                                      self.height // 3 * 2 - height_ // 2),
                                     (width_, height_),
                                     buttons,
                                     on_click_choose_character.to_main_menu)

        play_button = Button('Graphics/ChooseCharacter/PlayButton/basic.png',
                             'Graphics/ChooseCharacter/PlayButton/hovered_on.png',
                             (self.width // 2 - self.width // 5 - width // 2 + width_ + self.width // 50,
                              self.height // 3 * 2 - height_ // 2),
                             (width_, height_),
                             buttons,
                             on_click_choose_character.play)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/ChooseCharacter/Background/basic.jpg',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        # Initializing characters
        characters_group = pygame.sprite.Group()
        
        characters_names = []

        for filename in os.listdir("Data/Characters"):
            if os.path.splitext(filename)[-1] == ".json":
                characters_names.append(os.path.splitext(filename)[-2])

        character_index = 0
        characters = []

        for character_name in characters_names:
            characters.append(Player(character_name,
                                     characters_group,
                                     (self.width // 4, self.width // 4),
                                     (self.width // 2 - self.width // 8,
                                      self.height // 3 * 2 - height_ // 2 - self.width // 4)))

        # Initializing text boxes
        text_boxes = pygame.sprite.Group()

        character_name = TextBox(characters_names[character_index],
                                 pygame.font.Font("Fonts/Norse/bold.otf", self.width // 40),
                                 (self.width // 2,
                                  self.height // 3 * 2 - height_ // 2 - self.width // 4 - self.width // 40),
                                 text_boxes,
                                 (0, 0, 0),
                                 (255, 255, 255),
                                 (0, 0, 0))

        # Choose character loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            if not button.rect.collidepoint(pygame.mouse.get_pos()):
                                continue

                            if (button.on_click(character_index)[0] and 
                                    button.on_click(character_index)[1] is None):  # To main menu
                                return
                            else:
                                if button.on_click(character_index)[0]:  # Scroll Character
                                    character_index = button.on_click(character_index)[1]
                                    character_name.change_text(characters_names[character_index])
                                else:  # Play
                                    # Saving current character data
                                    with open(f"Data/Characters/{character_name.text}.json", "r") as file:
                                        data = json.load(file)

                                    with open(f"Data/CurrentCharacter/player.json", "w") as file:
                                        json.dump(data, file, indent=4)

                                    # Opening lobby map
                                    self.lobby()

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

            characters[character_index].draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def lobby(self):
        # Loading lobby map
        lobby_map = Map((self.width, self.height), self.screen)

        # Loading character data
        with open(f"Data/CurrentCharacter/player.json", "r") as file:
            data = json.load(file)
            character_name = data["name"]

        player_group = pygame.sprite.Group()
        player = Player(character_name,
                        player_group,
                        (self.height // 10, self.height // 10),
                        (0, 0))

        # Setting up camera
        camera = Camera((self.width, self.height))

        # Lobby loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.scancode == 41:
                        self.to_main_menu()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    on_click = lobby_map.on_click(pygame.mouse.get_pos(), player)

                    # Moving player to clicked tile by pixels
                    if on_click[0] == "move":
                        dx, dy = on_click[1]

                        while dx != 0 or dy != 0:
                            if dx > 0:
                                move = min(dx, player.width // 5)
                                player.rect.x += move
                                dx -= move
                            elif dx < 0:
                                move = min(dx * -1, player.width // 5)
                                player.rect.x -= move
                                dx += move

                            if dy > 0:
                                move = min(dy, player.height // 5)
                                player.rect.y += move
                                dy -= move
                            elif dy < 0:
                                move = min(dy * -1, player.height // 5)
                                player.rect.y -= move
                                dy += move

                            # Updating camera and moving sprites accordingly
                            camera.update(player)

                            for tile in lobby_map.tiles_group:
                                camera.apply(tile)

                            camera.apply(player)
                            for gear_element in player.gear_sprites:
                                gear_element.rect.x = player.rect.x
                                gear_element.rect.y = player.rect.y

                            # Updating screen
                            self.screen.fill((5, 50, 5))

                            lobby_map.render()
                            player.draw(self.screen)

                            pygame.display.flip()
                            self.clock.tick(FPS)

            # Updating camera and moving sprites accordingly
            camera.update(player)

            for tile in lobby_map.tiles_group:
                camera.apply(tile)

            camera.apply(player)
            for gear_element in player.gear_sprites:
                gear_element.rect.x = player.rect.x
                gear_element.rect.y = player.rect.y

            # Updating screen
            self.screen.fill((5, 50, 5))

            lobby_map.render()
            player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def to_main_menu(self):
        # Initializing buttons
        buttons = pygame.sprite.Group()

        width = self.width // 4
        height = self.height // 4

        to_main_menu_button = Button('Graphics/ToMainMenu/ToMainMenuButton/basic.png',
                                     'Graphics/ToMainMenu/ToMainMenuButton/hovered_on.png',
                                     (self.width // 8, self.height // 2 - height),
                                     (width, height),
                                     buttons,
                                     on_click_to_main_menu.to_main_menu)

        back_button = Button('Graphics/ToMainMenu/BackButton/basic.png',
                             'Graphics/ToMainMenu/BackButton/hovered_on.png',
                             (self.width // 8 * 5, self.height // 2 - height),
                             (width, height),
                             buttons,
                             on_click_to_main_menu.back)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/ToMainMenu/Background/basic.png',
                           (0, 0),
                           (self.width, self.height),
                           labels)
        # To main menu loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            if not button.rect.collidepoint(pygame.mouse.get_pos()):
                                continue

                            if button.on_click():  # To main menu
                                self.main_menu()
                            else:  # Back
                                return

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

            pygame.display.flip()
            self.clock.tick(FPS)


# Initializing all pygame modules
pygame.init()

# Starting game
game = Game()
game.main_menu()
