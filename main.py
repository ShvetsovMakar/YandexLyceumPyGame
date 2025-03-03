import pygame
import sys
import os
import json
import random

from Config.constants import *

from OnClickFunctions import (on_click_main_menu, on_click_add_character, on_click_choose_character,
                              on_click_to_main_menu, on_click_battle_ending)

from Sprites.Button import Button
from Sprites.Label import Label
from Sprites.TextBox import TextBox
from Sprites.InputBox import InputBox

from Sprites.Tile import Tile

from Sprites.Player.Player import Player

from Sprites.Mobs.Enemy import Enemy
from Sprites.Mobs.Merchant import Merchant
from Sprites.Mobs.Warrior import Warrior
from Sprites.Mobs.Forester import Forester

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
            self.board.append([])
            for x in range(len(field[y])):
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
        field_width = 64
        field_height = 64
        sub_paths_amount = 64

        obstacle_types = ["T"] * 8 + ["S"] * 2

        path_directions = ['U'] * 5 + ['D'] * 5 + ['R'] * 6
        sub_paths_directions = [['U'] * 20 + ['D'] * 4 + ['R'] * 6 + ['L'] * 4,
                                ['U'] * 20 + ['D'] * 4 + ['R'] * 4 + ['L'] * 6,
                                ['U'] * 4 + ['D'] * 20 + ['R'] * 6 + ['L'] * 4,
                                ['U'] * 4 + ['D'] * 20 + ['R'] * 4 + ['L'] * 6]
        last_direction = ''
        path = []
        x = 0
        y = random.randint(0, field_height - 1)

        field = [['O'] * field_width for _ in range(field_height)]
        field[y][0] = "G"

        # Generating main path
        while x < field_width - 1:
            direction = random.choice(path_directions)

            if direction == 'R':
                x += 1
                field[y][x] = 'G'
                path.append((y, x))
                last_direction = ''

            elif direction == 'D' and y < field_height - 1 and last_direction != 'U':
                y += 1
                field[y][x] = 'G'
                path.append((y, x))
                last_direction = 'D'

            elif direction == 'U' and y > 0 and last_direction != 'D':
                y -= 1
                field[y][x] = 'G'
                path.append((y, x))
                last_direction = 'U'
                
        del path[-1]
        sub_paths = []

        # Generating sub paths
        for i in range(sub_paths_amount):
            if i > 5:
                choice = []
                choice.append(random.choice(path))

                for i in range(10):
                    choice.append(random.choice(sub_paths))

                start = random.choice(choice)
            else:
                start = random.choice(path)

            y, x = start
            last_direction = ''

            cur_directions = random.choice(sub_paths_directions)

            for j in range(random.randint(field_width // 2, field_width)):
                direction = random.choice(cur_directions)

                if direction == 'R' and last_direction != 'L' and x <= field_width - 2:
                    x += 1
                    field[y][x] = 'G'
                    sub_paths.append((y, x))
                    last_direction = 'R'

                elif direction == 'L' and last_direction != 'R' and x >= 1:
                    x -= 1
                    field[y][x] = 'G'
                    sub_paths.append((y, x))
                    last_direction = 'L'

                elif direction == 'D' and last_direction != 'U' and y <= field_height - 2:
                    y += 1
                    field[y][x] = 'G'
                    sub_paths.append((y, x))
                    last_direction = 'D'

                elif direction == 'U' and last_direction != 'D' and y >= 1:
                    y -= 1
                    field[y][x] = 'G'
                    sub_paths.append((y, x))
                    last_direction = 'U'
            
        # Differentiating obstacles
        for y in range(field_height):
            for x in range(field_width):
                if field[y][x] == "O":
                    field[y][x] = random.choice(obstacle_types)

        return [''.join(line) for line in field]

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

    def on_click(self, mouse_pos, player, mobs_group, camera, clock):
        tile = self.get_tile(mouse_pos)

        if tile is None:
            return

        # Defining player and tile position on the map
        player_pos = [player.rect.x // self.tile_width, player.rect.y // self.tile_height]
        tile_pos = [tile.rect.x // self.tile_width, tile.rect.y // self.tile_height]

        # Checking if player is able to move to this tile
        if not (-1 <= player_pos[0] - tile_pos[0] <= 1 and -1 <= player_pos[1] - tile_pos[1] <= 1 and tile.walkable):
            return

        # Checking if player has clicked on mob
        for mob in mobs_group:
            if mob.rect.x == tile.rect.x and mob.rect.y == tile.rect.y:
                return mob.on_click(player)

        # Moving player to clicked tile by pixels
        dx = tile.rect.x - player.rect.x
        dy = tile.rect.y - player.rect.y

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

            for tile in self.tiles_group:
                camera.apply(tile)

            for mob in mobs_group:
                camera.apply(mob)

            camera.apply(player)
            for gear_element in player.gear_sprites:
                gear_element.rect.x = player.rect.x
                gear_element.rect.y = player.rect.y

            # Updating screen
            self.screen.fill(GREEN_BACKGROUND)

            self.render()
            mobs_group.draw(self.screen)
            player.draw(self.screen)

            pygame.display.flip()
            clock.tick(FPS)


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

        # Creating mobs
        mobs_group = pygame.sprite.Group()

        merchant = Merchant("Graphics/Villagers/Merchant.png",
                            (self.height // 10 * MERCHANT_POSITION[1],
                             self.height // 10 * MERCHANT_POSITION[0]),
                            (self.height // 10, self.height // 10),
                            mobs_group)

        warrior = Warrior("Graphics/Villagers/Warrior.png",
                          (self.height // 10 * VILLAGER_POSITION[1],
                           self.height // 10 * VILLAGER_POSITION[0]),
                          (self.height // 10, self.height // 10),
                          mobs_group)

        # Lobby loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.scancode == 41:
                        self.to_main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    on_click = lobby_map.on_click(pygame.mouse.get_pos(), player, mobs_group, camera, self.clock)
                    if on_click == "forest":
                        self.battle(on_click)

            # Updating camera and moving sprites accordingly
            camera.update(player)

            for tile in lobby_map.tiles_group:
                camera.apply(tile)

            for mob in mobs_group:
                camera.apply(mob)

            camera.apply(player)
            for gear_element in player.gear_sprites:
                gear_element.rect.x = player.rect.x
                gear_element.rect.y = player.rect.y

            # Updating screen
            self.screen.fill(GREEN_BACKGROUND)

            lobby_map.render()
            mobs_group.draw(self.screen)
            player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def battle(self, field):
        # Loading battle map
        battle_map = Map((self.width, self.height), self.screen, field=field)

        # Loading character data
        with open(f"Data/CurrentCharacter/player.json", "r") as file:
            data = json.load(file)
            character_name = data["name"]

        # Determining player's position on the battle map
        walkable_tiles = []
        for y in range(len(battle_map.board)):
            if battle_map.board[y][0].walkable:
                walkable_tiles.append((battle_map.board[y][0].rect.x, battle_map.board[y][0].rect.y))

        player_group = pygame.sprite.Group()
        player = Player(character_name,
                        player_group,
                        (self.height // 10, self.height // 10),
                        random.choice(walkable_tiles))

        # Setting up camera
        camera = Camera((self.width, self.height))

        # Creating mobs
        mobs_group = pygame.sprite.Group()
        enemies = []

        # Determining forester's position on the battle map
        walkable_tiles = []
        for y in range(len(battle_map.board)):
            if battle_map.board[y][len(battle_map.board[y]) - 1].walkable:
                walkable_tiles.append((battle_map.board[y][-1].rect.x, battle_map.board[y][-1].rect.y))

        forester = Forester("Graphics/Villagers/Forester.png",
                            random.choice(walkable_tiles),
                            (self.height // 10, self.height // 10),
                            mobs_group)

        # Determining enemies positions
        walkable_tiles = []
        for y in range(len(battle_map.board)):
            for x in range(len(battle_map.board[y])):
                if battle_map.board[y][x].walkable:
                    walkable_tiles.append((battle_map.board[y][x].rect.x, battle_map.board[y][x].rect.y))
        walkable_tiles.remove((player.rect.x, player.rect.y))
        walkable_tiles.remove((forester.rect.x, forester.rect.y))

        for i in range(min(len(walkable_tiles) // 2, ENEMIES_AMOUNT)):
            position = random.choice(walkable_tiles)
            walkable_tiles.remove(position)

            enemy_type = random.choice(ENEMIES)

            enemies.append(Enemy(f"Graphics/Enemies/{enemy_type}.png",
                                 position,
                                 (self.height // 10, self.height // 10),
                                 mobs_group,
                                 ENEMIES_DAMAGE[enemy_type],
                                 ENEMIES_HEALTH[enemy_type]))

        # Battle loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.scancode == 41:
                        self.to_main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    on_click = battle_map.on_click(pygame.mouse.get_pos(), player, mobs_group, camera, self.clock)
                    if on_click == "exit":
                        self.battle_ending(player)

                    # Moving enemies
                    for enemy in enemies:
                        if enemy.health <= 0:
                            continue

                        # Determining enemy's position on the board
                        for y in range(len(battle_map.board)):
                            for x in range(len(battle_map.board[y])):
                                if (battle_map.board[y][x].rect.x == enemy.rect.x and
                                        battle_map.board[y][x].rect.y == enemy.rect.y):
                                    enemy_board_pos = (y, x)
                                    break

                        # Determining walkable tiles
                        walkable_tiles = []
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                y = enemy_board_pos[0] + dy
                                x = enemy_board_pos[1] + dx

                                if y < 0 or y >= len(battle_map.board):
                                    continue

                                if x < 0 or x >= len(battle_map.board[y]):
                                    continue

                                if battle_map.board[y][x].walkable:
                                    walkable_tiles.append(battle_map.board[y][x])

                        # Checking if enemy can hit the player
                        for tile in walkable_tiles:
                            if tile.rect.x == player.rect.x and tile.rect.y == player.rect.y:
                                agility = player.agility
                                protection = 0

                                gear_elements = [player.helmet, player.breastplate, player.leggings]
                                for gear_element in gear_elements:
                                    if gear_element is not None:
                                        agility += gear_element.agility
                                        protection += gear_element.protection

                                if agility >= random.randint(1, 101):
                                    continue

                                player.health -= enemy.damage * (1 - protection)
                                if player.health <= 0:
                                    self.defeat()
                                break

                        else:
                            # Removing tiles with mobs
                            for mob in mobs_group:
                                for tile in walkable_tiles:
                                    if mob.rect.x == tile.rect.x and mob.rect.y == tile.rect.y:
                                        if mob in enemies and mob.health <= 0:
                                            continue

                                        walkable_tiles.remove(tile)
                                        break

                            if walkable_tiles:
                                tile = random.choice(walkable_tiles)
                                enemy.move(tile.rect.x, tile.rect.y)

            # Updating camera and moving sprites accordingly
            camera.update(player)

            for tile in battle_map.tiles_group:
                camera.apply(tile)

            for mob in mobs_group:
                camera.apply(mob)

            camera.apply(player)
            for gear_element in player.gear_sprites:
                gear_element.rect.x = player.rect.x
                gear_element.rect.y = player.rect.y

            # Updating screen
            self.screen.fill(GREEN_BACKGROUND)

            battle_map.render()
            mobs_group.draw(self.screen)
            player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def defeat(self):
        # Initializing buttons
        buttons = pygame.sprite.Group()

        width = self.width // 4
        height = self.height // 4

        to_main_menu_button = Button('Graphics/Defeat/ToMainMenuButton/basic.png',
                                     'Graphics/Defeat/ToMainMenuButton/hovered_on.png',
                                     (self.width // 8, self.height // 2 - height),
                                     (width, height),
                                     buttons,
                                     on_click_battle_ending.to_main_menu)

        to_lobby_button = Button('Graphics/Defeat/ToLobbyButton/basic.png',
                                 'Graphics/Defeat/ToLobbyButton/hovered_on.png',
                                 (self.width // 8 * 5, self.height // 2 - height),
                                 (width, height),
                                 buttons,
                                 on_click_battle_ending.to_lobby)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/Defeat/Background/basic.png',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        # Initializing text boxes
        text_boxes = pygame.sprite.Group()

        collected_gold = TextBox(f"Game Over!",
                                 pygame.font.Font("Fonts/Norse/bold.otf", self.width // 40),
                                 (self.width // 2, self.height // 2 - self.height // 4 - self.width // 40),
                                 text_boxes,
                                 (255, 0, 0),
                                 (255, 255, 255),
                                 (0, 0, 0))

        # Defeat loop
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

                            if button.on_click():  # To lobby
                                self.lobby()
                            else:  # To main menu
                                self.main_menu()

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

            pygame.display.flip()
            self.clock.tick(FPS)

    def battle_ending(self, player):
        # Determining the amount of collected gold
        with open(f"Data/CurrentCharacter/player.json", "r") as file:
            data = json.load(file)
            gold = player.gold - data["gold"]
        player.save()

        # Initializing buttons
        buttons = pygame.sprite.Group()

        width = self.width // 4
        height = self.height // 4

        to_main_menu_button = Button('Graphics/BattleEnding/ToMainMenuButton/basic.png',
                                     'Graphics/BattleEnding/ToMainMenuButton/hovered_on.png',
                                     (self.width // 8, self.height // 2 - height),
                                     (width, height),
                                     buttons,
                                     on_click_battle_ending.to_main_menu)

        to_lobby_button = Button('Graphics/BattleEnding/ToLobbyButton/basic.png',
                                 'Graphics/BattleEnding/ToLobbyButton/hovered_on.png',
                                 (self.width // 8 * 5, self.height // 2 - height),
                                 (width, height),
                                 buttons,
                                 on_click_battle_ending.to_lobby)

        # Initializing labels
        labels = pygame.sprite.Group()

        background = Label('Graphics/BattleEnding/Background/basic.png',
                           (0, 0),
                           (self.width, self.height),
                           labels)

        # Initializing text boxes
        text_boxes = pygame.sprite.Group()

        collected_gold = TextBox(f"{gold} gold collected!",
                                 pygame.font.Font("Fonts/Norse/bold.otf", self.width // 40),
                                 (self.width // 2, self.height // 2 - self.height // 4 - self.width // 40),
                                 text_boxes,
                                 (0, 0, 0),
                                 (255, 255, 255),
                                 (0, 0, 0))

        # Battle ending loop
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

                            if button.on_click():  # To lobby
                                self.lobby()
                            else:  # To main menu
                                self.main_menu()

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
