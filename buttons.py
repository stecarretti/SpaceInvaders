import pygame as pg
from object import Button, BLACK_COLOR

IMAGES_PATH = 'images\\'


class RectButton(Button):

    def __init__(self, color, x, y, width, height, text=''):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pg.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, BLACK_COLOR)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)))


class ImageButton(Button):
    def __init__(self, img, x, y, width, height):
        super().__init__(x, y, width, height)
        img = pg.image.load(img)
        self.image = pg.transform.scale(img, (self.width, self.height))

    def draw(self, background):
        background.blit(self.image, (self.x, self.y))


class ArrowButton(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, background):
        img = pg.draw.polygon(background, (0, 0, 0),
                              ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
        # surface = pg.image.load(IMAGES_PATH + 'black.jpg')
        # surface.blit(img)
        # arrow = pg.transform.scale(surface, (self.width, self.height))
        # background.blit(arrow, (self.x, self.y))

        surface = pg.Surface((200, 200))
        img.draw(surface)
        arrow = pg.transform.scale(surface, (self.width, self.height))
        background.blit(arrow)


