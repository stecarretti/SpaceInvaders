import pygame as pg

# Colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
BUTTON_COLOR = (73, 106, 168)
BUTTON_COVERED_COLOR = (76, 134, 199)


class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pg.image.load(image_path)
        self.image = pg.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class ScreenObject:

    def __init__(self, icon_img, img, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        self.game_screen = pg.display.set_mode((self.width, self.height))
        self.game_screen.fill(WHITE_COLOR)
        pg.display.set_caption(self.title)
        icon = pg.image.load(icon_img)
        pg.display.set_icon(icon)
        
        background_img = pg.image.load(img)
        self.image = pg.transform.scale(background_img, (self.width, self.height))


class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
