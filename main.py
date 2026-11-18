from game import Game
from states import MenuState


def main():
    game = Game()
    game.run(MenuState(game))


if __name__ == "__main__":
    main()