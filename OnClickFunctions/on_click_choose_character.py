import os


def forward(character_index):
    return True, (character_index + 1) % len(os.listdir("Data/Characters"))


def backward(character_index):
    return True, (character_index - 1) % len(os.listdir("Data/Characters"))


def to_main_menu(character_index):
    return True, None

def play(character_index):
    return False, None
