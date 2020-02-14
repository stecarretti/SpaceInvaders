import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (48, 66, 89)
LIGHT_BLUE = (32, 102, 149)
LIGHT_LIGHT_BLUE = (118, 167, 199)
YELLOW = (165, 152, 48)


# --- Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    # number of lives (plus 1 because 0 is still a life)
    life = 2
    colors = [LIGHT_LIGHT_BLUE, LIGHT_BLUE, BLUE]

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.width = 80
        self.height = 15

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colors[self.life])

        self.rect = self.image.get_rect()

    def hit(self):
        if self.life == 0:
            return True
        self.life -= 1
        self.image.fill(self.colors[self.life])
        return False



class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self, type):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.width = 5
        self.height = 13
        self.type = type

        self.image = pygame.Surface([self.width, self.height])
        if self.type == 0:
            self.image.fill(WHITE)
        else:
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        if self.type == 0:
            self.rect.y -= 8
        else:
            self.rect.y += 8

#
# # --- Create the window
#
# # Initialize Pygame
# pygame.init()
#
# # Set the height and width of the screen
# screen_width = 700
# screen_height = 400
# screen = pygame.display.set_mode([screen_width, screen_height])
#
# # --- Sprite lists
#
# # This is a list of every sprite. All blocks and the player block as well.
# all_sprites_list = pygame.sprite.Group()
#
# # List of each block in the game
# block_list = pygame.sprite.Group()
#
# # List of each bullet
# bullet_list = pygame.sprite.Group()
#
# # --- Create the sprites
#
# for i in range(50):
#     # This represents a block
#     block = Block(BLUE)
#
#     # Set a random location for the block
#     block.rect.x = random.randrange(screen_width)
#     block.rect.y = random.randrange(350)
#
#     # Add the block to the list of objects
#     block_list.add(block)
#     all_sprites_list.add(block)
#
# # Create a red player block
# player = Player()
# all_sprites_list.add(player)
#
# # Loop until the user clicks the close button.
# done = False
#
# # Used to manage how fast the screen updates
# clock = pygame.time.Clock()
#
# score = 0
# player.rect.y = 370
#
# # -------- Main Program Loop -----------
# while not done:
#     # --- Event Processing
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             # Fire a bullet if the user clicks the mouse button
#             bullet = Bullet()
#             # Set the bullet so it is where the player is
#             bullet.rect.x = player.rect.x
#             bullet.rect.y = player.rect.y
#             # Add the bullet to the lists
#             all_sprites_list.add(bullet)
#             bullet_list.add(bullet)
#
#     # --- Game logic
#
#     # Call the update() method on all the sprites
#     all_sprites_list.update()
#
#     # Calculate mechanics for each bullet
#     for bullet in bullet_list:
#
#         # See if it hit a block
#         block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
#
#         # For each block hit, remove the bullet and add to the score
#         for block in block_hit_list:
#             bullet_list.remove(bullet)
#             all_sprites_list.remove(bullet)
#             score += 1
#             print(score)
#
#         # Remove the bullet if it flies up off the screen
#         if bullet.rect.y < -10:
#             bullet_list.remove(bullet)
#             all_sprites_list.remove(bullet)
#
#     # --- Draw a frame
#
#     # Clear the screen
#     screen.fill(WHITE)
#
#     # Draw all the spites
#     all_sprites_list.draw(screen)
#
#     # Go ahead and update the screen with what we've drawn.
#     pygame.display.flip()
#
#     # --- Limit to 20 frames per second
#     clock.tick(60)
#
# pygame.quit()