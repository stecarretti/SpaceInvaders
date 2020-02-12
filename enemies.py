from object import GameObject
import random


class Enemy(GameObject):

    SPEED = 1.5

    def __init__(self, image_path, level):
        self.SPEED += level
        self.width = 35
        self.height = 35
        super().__init__(image_path, 0, 0, self.width, self.height)

    def set_position(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def move(self, max_width, level):
        if self.x_pos <= 10:
            self.SPEED = abs(self.SPEED)
            self.y_pos += self.height + 50 * level
        elif self.x_pos > max_width - self.width - 10:
            self.SPEED = -abs(self.SPEED)
            self.y_pos += self.height + 50 * level
        self.x_pos += self.SPEED
        if self.y_pos >= 600:
            return True
        else:
            return False

    def detect_collision(self, bullet):
        if self.y_pos > bullet.rect.y + bullet.height - self.height * 0.3:
            return False
        elif self.y_pos + self.height < bullet.rect.y + self.height * 0.3:
            return False

        if self.x_pos > bullet.rect.x + bullet.width - self.height * 0.3:
            return False
        elif self.x_pos + self.width < bullet.rect.x + self.height * 0.3:
            return False

        return True
