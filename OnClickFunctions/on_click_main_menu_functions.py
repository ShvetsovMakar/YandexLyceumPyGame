import pygame
import sys

def exit_button(game):
    pygame.quit()
    sys.exit()

def add_character_button(game):
    game.add_character()


def play_button(game):
    game.play()
