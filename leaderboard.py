import pandas as pd
import pygame as pg
from object import ScreenObject, WHITE_COLOR
from game import redraw_window_and_click
from buttons import ImageButton


IMAGES_PATH = 'images\\'
TITLES_COLOR = (44, 157, 58)


class Leaderboard(ScreenObject):

    TICK_RATE = 60

    def __init__(self, img, file, title, width, height):
        super().__init__(img, title, width, height)
        self.file = file
        self.df = pd.read_csv(file)
        self.df = self.df.sort_values(by=['Score'], ascending=False)
        self.back_button = ImageButton(IMAGES_PATH + 'arrow.png', 20, 20, 70, 70)

    def draw(self):

        font = pg.font.SysFont('comicsans', 40)
        font_titles = pg.font.SysFont('comicsans', 60)

        self.game_screen.blit(self.image, (0, 0))
        self.back_button.draw(self.game_screen)

        text = font_titles.render('User', True, TITLES_COLOR)
        self.game_screen.blit(text, (self.width / 2 - 250, 80))

        text = font_titles.render('Score', True, TITLES_COLOR)
        self.game_screen.blit(text, (self.width / 2 + 50, 80))

        x = self.width/2 - 250
        y = 180

        for index, row in self.df.iterrows():
            user = font.render(str(row['User']), 1, WHITE_COLOR)
            self.game_screen.blit(user, (x, y))
            x += 300
            score = font.render(str(row['Score']), 1, WHITE_COLOR)
            self.game_screen.blit(score, (x, y))
            y += 45
            x = self.width/2 - 250
            if y > self.height:
                break

        run = True

        while run:
            for event in pg.event.get():
                pos = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_button.isOver(pos):
                        return 0
                # print(event)
            redraw_window_and_click(self.TICK_RATE)
