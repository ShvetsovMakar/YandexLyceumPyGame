def forward(game, index):
    return False, (index + 1) % 4


def backward(game, index):
    return False, (index - 1) % 4


def to_main_menu(game, index):
    return (True, )


def create_character(game, index):
    return False, index
