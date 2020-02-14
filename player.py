import pygame as pg
from object import GameObject

IMAGES_PATH = 'images\\'
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 735
SCREEN_TITLE = 'Space Invaders'
# Colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
clock = pg.time.Clock()
pg.font.init()
font = pg.font.SysFont('comicsans', 75)


class PlayerCharacter(GameObject):

    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move_y(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        # set minimum position of the character
        if self.y_pos >= max_height - self.height - 10:
            self.y_pos = max_height - self.height - 10
        # set maximum position of the character
        if self.y_pos <= 5:
            self.y_pos = 5

    def move_x(self, direction, max_width):
        if direction > 0:
            self.x_pos -= self.SPEED
        elif direction < 0:
            self.x_pos += self.SPEED

        # set maximum right position of the character
        if self.x_pos >= max_width - self.width - 10:
            self.x_pos = max_width - self.width - 10
        # set maximum left position of the character
        if self.x_pos <= 5:
            self.x_pos = 5

    def fire(self, background):
        pg.draw.rect(background, WHITE_COLOR, [self.x_pos, self.y_pos + self.height, 5, 10])

    def detect_collision(self, bullet):
        if self.y_pos > bullet.rect.y + bullet.height - self.height * 0.33:
            return False
        elif self.y_pos + self.height < bullet.rect.y + self.height * 0.2:
            return False

        if self.x_pos > bullet.rect.x + bullet.width - 3:
            return False
        elif self.x_pos + self.width < bullet.rect.x + 3:
            return False

        return True
