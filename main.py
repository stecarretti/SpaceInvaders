import pygame as pg
import os
from game import Game, StartScreen
from leaderboard import Leaderboard


IMAGES_PATH = 'images\\'
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 735
SCREEN_TITLE = 'Space Invaders'


def main():
    # set window position
    a = 3
    b = 23
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (a, b)

    file = 'scores.csv'

    pg.init()

    pg.mixer.music.load('sounds/background.wav')
    pg.mixer.music.play(-1)

    start_screen = StartScreen(IMAGES_PATH + 'shuttle.ico', IMAGES_PATH + 'galaxy.jpg', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    action = start_screen.get_action()

    while action != 3:
        if action == 0:
            new_game = Game(IMAGES_PATH + 'shuttle.ico', file, IMAGES_PATH + 'galaxy.jpg', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
            new_game.run_game_loop(0, 0)
            pg.mixer.music.load('sounds/background.wav')
            pg.mixer.music.play(-1)
        elif action == 1:
            # show leaderboard
            leaderboard = Leaderboard(IMAGES_PATH + 'shuttle.ico', IMAGES_PATH + 'galaxy.jpg', file, SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
            leaderboard.draw()
        action = start_screen.get_action()

    pg.quit()
    quit()


# entry point
if __name__ == '__main__':
    main()
