import pygame as pg

import random
import math
from sprites import Bullet, Block
from enemies import Enemy
from player import PlayerCharacter
from object import ScreenObject, BUTTON_COLOR, BUTTON_COVERED_COLOR, WHITE_COLOR
from buttons import RectButton


IMAGES_PATH = 'images\\'
# Colors according to RGB codes
TITLES_COLOR = (44, 157, 58)
COMMANDS_COLOR = (82, 126, 228)
clock = pg.time.Clock()
pg.font.init()
font = pg.font.SysFont('comicsans', 75)
font_score = pg.font.SysFont('comicsans', 40)


def redraw_window_and_click(tick_rate):
    pg.display.update()
    clock.tick(tick_rate)


class StartScreen(ScreenObject):

    TICK_RATE = 60

    def __init__(self, icon_img, img, title, width, height):
        super().__init__(icon_img, img, title, width, height)
        self.game_button = RectButton(BUTTON_COLOR, self.width/2 - 90, 130, 180, 100, 'Start')
        self.leaderboard_button = RectButton(BUTTON_COLOR, self.width/2 - 125, 370, 250, 100, 'Leaderboard')
        self.instructions = ['Commands',
                             'Move               -->    left and right arrow',
                             'Fire                 -->    space',
                             'Constant fire  -->    down arrow',
                             'Pause             -->    up arrow',
                             'Unpause         -->    up arrow']

    def get_action(self):
        font1 = pg.font.SysFont('comicsans', 45)
        font2 = pg.font.SysFont('comicsans', 30)
        run = True

        while run:
            for event in pg.event.get():
                pos = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.game_button.isOver(pos):
                        return 0
                    elif self.leaderboard_button.isOver(pos):
                        return 1
                if event.type == pg.MOUSEMOTION:
                    if not self.game_button.isOver(pos):
                        self.game_button.color = BUTTON_COLOR
                    if not self.leaderboard_button.isOver(pos):
                        self.leaderboard_button.color = BUTTON_COLOR
                    if self.game_button.isOver(pos):
                        self.game_button.color = BUTTON_COVERED_COLOR
                    elif self.leaderboard_button.isOver(pos):
                        self.leaderboard_button.color = BUTTON_COVERED_COLOR
                # print(event)

            self.game_screen.blit(self.image, (0, 0))
            for count, instr in enumerate(self.instructions):
                y = self.height-200+30*count
                if count == 0:
                    instruction = font1.render(instr, 1, BUTTON_COLOR)
                    y -= 20
                else:
                    instruction = font2.render(instr, 1, BUTTON_COVERED_COLOR)
                self.game_screen.blit(instruction, (15, y))
            self.game_button.draw(self.game_screen)
            self.leaderboard_button.draw(self.game_screen)
            redraw_window_and_click(self.TICK_RATE)


class Game(ScreenObject):

    TICK_RATE = 60

    def __init__(self, icon_img, file, img, title, width, height):
        super().__init__(icon_img, img, title, width, height)
        self.file = file

    def run_game_loop(self, level, score):
        is_game_over = False
        did_win = False
        direction = 0
        # Variables to control enemy's fire rate
        enemy_reload_speed = 400 - round(80 * level)
        enemy_reloaded_event = pg.USEREVENT + 1
        enemy_reloaded = True
        # If True player fires automatically
        constant_fire = False
        player_reload_speed = 150 - round(10 * level)
        player_reloaded_event = pg.USEREVENT + 2
        player_reloaded = True
        # If True game is paused
        pause = False

        player = PlayerCharacter(IMAGES_PATH + 'space-ship-icon.png', self.width/2 - 30, 650, 50, 50)

        # This is a list of every sprite. All blocks and the player block as well.
        all_sprites_list = pg.sprite.Group()

        # List of player bullet
        bullet_player_list = pg.sprite.Group()

        # List of enemies bullets
        bullet_enemies_list = pg.sprite.Group()

        enemies_list = self.initialize_enemies(level)

        block_list, all_sprites_list = self.initialize_blocks(all_sprites_list)

        while not is_game_over:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_game_over = True
                # detect when any key is pressed down
                elif event.type == pg.KEYDOWN and not constant_fire:
                    # UP key is used to stop and unstop the game
                    if event.key == pg.K_UP:
                        pause = not pause
                        if pause:
                            pg.mixer.music.pause()
                        else:
                            pg.mixer.music.unpause()
                    elif event.key == pg.K_DOWN:
                        constant_fire = True
                        player_reloaded = True
                        pg.time.set_timer(player_reloaded_event, 0)
                    elif event.key == pg.K_LEFT:
                        direction = 1
                    elif event.key == pg.K_RIGHT:
                        direction = -1
                    elif event.key == pg.K_SPACE:
                        # Fire a bullet if the user clicks the space button
                        bullet = Bullet(0)
                        # Set the bullet so it is where the player is
                        bullet.rect.x = player.x_pos + player.width / 2
                        bullet.rect.y = player.y_pos
                        # Add the bullet to the lists
                        all_sprites_list.add(bullet)
                        bullet_player_list.add(bullet)
                # detect when any key is released
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_RIGHT or pg.K_LEFT:
                        direction = 0
                    if event.key == pg.K_DOWN:
                        constant_fire = False
                elif event.type == enemy_reloaded_event:
                    # when the reload timer runs out, reset it
                    enemy_reloaded = True
                    pg.time.set_timer(enemy_reloaded_event, 0)
                elif event.type == player_reloaded_event and constant_fire:
                    player_reloaded = True
                    pg.time.set_timer(player_reloaded_event, 0)
                # print(event)

            # Calculate mechanics for each bullet
            for bullet in bullet_player_list:

                # If level is greater than 3, player can fire through the blocks
                if level < 3.5:
                    # See if it hit a block
                    block_hit_list = pg.sprite.spritecollide(bullet, block_list, False)

                    # For each block hit, remove the bullet
                    for block in block_hit_list:
                        if block.hit():
                            block_list.remove(block)
                            all_sprites_list.remove(block)
                        bullet_player_list.remove(bullet)
                        all_sprites_list.remove(bullet)

                for e in enemies_list:
                    if e.detect_collision(bullet):
                        score += 1 + math.ceil(level * 10)
                        bullet_player_list.remove(bullet)
                        all_sprites_list.remove(bullet)
                        enemies_list.remove(e)

                # Remove the bullet if it flies up off the screen
                if bullet.rect.y < -10:
                    bullet_player_list.remove(bullet)
                    all_sprites_list.remove(bullet)

            for bullet in bullet_enemies_list:
                # See if it hit a block
                block_hit_list = pg.sprite.spritecollide(bullet, block_list, False)

                # For each block hit, remove the bullet and add to the score
                for block in block_hit_list:
                    if block.hit():
                        block_list.remove(block)
                        all_sprites_list.remove(block)
                    bullet_enemies_list.remove(bullet)
                    all_sprites_list.remove(bullet)

                if player.detect_collision(bullet):
                    pg.mixer.music.load('sounds/crash.wav')
                    pg.mixer.music.play(0)
                    text = font.render('YOU LOST', True, WHITE_COLOR)
                    self.game_screen.blit(text, (540, 300))
                    pg.display.update()
                    clock.tick(1)
                    self.add_score(score)
                    return

                # Remove the bullet if it flies up off the screen
                if bullet.rect.y > 700:
                    bullet_enemies_list.remove(bullet)
                    all_sprites_list.remove(bullet)

            if not pause:
                # reset screen
                self.game_screen.fill(WHITE_COLOR)
                self.game_screen.blit(self.image, (0, 0))

                # move and draw player
                player.move_x(direction, self.width)
                player.draw(self.game_screen)

                # fire automatically if constant_fire
                if constant_fire and player_reloaded:
                    bullet = Bullet(0)
                    # Set the bullet so it is where the player is
                    bullet.rect.x = player.x_pos + player.width / 2
                    bullet.rect.y = player.y_pos
                    # Add the bullet to the lists
                    all_sprites_list.add(bullet)
                    bullet_player_list.add(bullet)
                    player_reloaded = False
                    # when shooting, create a timeout of RELOAD_SPEED
                    pg.time.set_timer(player_reloaded_event, player_reload_speed)

                # move enemies
                for i, e in enumerate(enemies_list):
                    if e.move(self.width, level):
                        text = font.render('YOU LOST', True, WHITE_COLOR)
                        self.game_screen.blit(text, (540, 300))
                        self.add_score(score)
                        pg.display.update()
                        clock.tick(1)
                        return
                    e.draw(self.game_screen)

                    # enemy fires or not with a certain probability
                    if random.random() <= 0.2:
                        if enemy_reloaded:
                            enemy_reloaded = False
                            # create a timeout of reload_speed
                            pg.time.set_timer(enemy_reloaded_event, enemy_reload_speed)
                            # Fire a bullet if the user clicks the mouse button
                            bullet = Bullet(1)
                            # Set the bullet so it is where the player is
                            bullet.rect.x = e.x_pos + e.width / 2
                            bullet.rect.y = e.y_pos
                            # Add the bullet to the lists
                            all_sprites_list.add(bullet)
                            bullet_enemies_list.add(bullet)

                self.move_all_sprites(all_sprites_list)

                if self.check_win(enemies_list):
                    did_win = True
                    break

                # update score
                text = font_score.render(str(score), 1, WHITE_COLOR)
                self.game_screen.blit(text, (self.width - 90, 14))

            redraw_window_and_click(self.TICK_RATE)

        if did_win:
            self.run_game_loop(level + 0.5, score)
        else:
            return

    def initialize_enemies(self, level):

        enemies_list = []

        for i in range(45):
            if i < 15:
                j = i
            elif i < 30:
                j = i - 15
            else:
                j = i - 30
            enemy = Enemy(IMAGES_PATH + 'UFO-icon.png', level)
            x = 20 + j * enemy.width * 1.3
            y = math.floor(i / 15) * 65 + 18
            enemy.set_position(x, y)
            enemies_list.append(enemy)

        return enemies_list

    def initialize_blocks(self, all_sprites_list):

        block_list = pg.sprite.Group()

        for i in range(20):

            block = Block()
            # Set location for the block
            if i / 10 < 1:
                block.rect.x = math.floor(i / 2) * 280 + 20 + i % 2 * block.width * 1.3
                block.rect.y = 550
            else:
                block.rect.x = math.floor((i-10) / 2) * 280 + 20 + (i-10) % 2 * block.width * 1.3
                block.rect.y = 550 + block.height + 5

            # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)

        return [block_list, all_sprites_list]

    def move_all_sprites(self, all_sprites_list):
        all_sprites_list.update()
        all_sprites_list.draw(self.game_screen)

    def check_win(self, enemies_list):
        if enemies_list.__len__() == 0:
            text = font.render('YOU WON', True, WHITE_COLOR)
            self.game_screen.blit(text, (540, 300))
            pg.display.update()
            clock.tick(1)
            return True
        return False

    def add_score(self, score):
        user = ''
        not_done = True
        delete = False
        while not_done:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.unicode.isalpha():
                        if len(user) <= 18:
                            user += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        delete = True
                    elif event.key == pg.K_RETURN:
                        not_done = False
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_BACKSPACE:
                        delete = False
                elif event.type == pg.QUIT:
                    return
            # In this way if the user holds the backspace, the word lenght will keep decreasing
            if delete:
                user = user[:-1]
            
            # Blit text for user input and visualize score
            self.game_screen.blit(self.image, (0, 0))
            text = font.render('Enter your name', True, WHITE_COLOR)
            self.game_screen.blit(text, (self.width/2 - 195, 150))
            block = font.render(user, True, TITLES_COLOR)
            rect = block.get_rect()
            rect.center = self.game_screen.get_rect().center
            self.game_screen.blit(block, rect)
            text_score = font.render('Your score: ' + str(score), True, WHITE_COLOR)
            self.game_screen.blit(text_score, (self.width/2 - 175, self.height-150))
            redraw_window_and_click(15)

        file = open(self.file, "a+")
        string = user + ',' + str(score) + '\n'
        file.write(string)
        file.close()

