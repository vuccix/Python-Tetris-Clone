"""
This is the game module responsible for the Tetris game logic
"""

from random import choice
from os import path

# component
from settings import (
    pg, GAME_W, GAME_H, PADDING, SIDEBAR_W, COLOURS, COLUMNS, ROWS, TETROMINOS, MOVE_DOWN_SPEED, SIDE_MOVE_DELAY,
    ROTATE_DELAY, SCORE_POINTS, LINE_COLOUR, CELL, BG_GAME_COLOUR, OUTLINE_COLOUR
)
from Game_Logic.tetromino import Tetromino
from Game_Logic.timer import Timer


class Game:
    """
    The game class is responsible for all the game logic.
    This class renders the game and manages the game logic and loop
    """
    def __init__(self, get_next: (), update_score: ()):
        """
        Initialize the game class.
        This method sets up the game, initializes timers, and loads assets
        """
        self.surface = pg.Surface((GAME_W, GAME_H))
        self.screen = pg.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING * 2 + SIDEBAR_W, PADDING))
        self.sprite_group = pg.sprite.Group()

        self.get_next = get_next
        self.update_score = update_score

        # game over screen
        self.text_bg_colour = choice(list(COLOURS))
        self.fonts = [
            pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 60),
            pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 25)
        ]

        # grid
        self.line = self.surface.copy()
        self.line.fill((0, 200, 0))
        self.line.set_colorkey((0, 200, 0))

        # tetrominos
        self.game_area = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprite_group, self.create_tetromino, self.game_area)

        # game clock
        self.down_speed = MOVE_DOWN_SPEED
        self.down_speed_faster = SIDE_MOVE_DELAY

        self.timers = {
            'horizontal': Timer(SIDE_MOVE_DELAY),
            'vertical': Timer(self.down_speed, True, self.move_down),
            'rotation': Timer(ROTATE_DELAY),
        }
        self.timers['vertical'].activate()

        # bool values
        self.bools = {
            'paused': False,
            'down': False,
            'space': False,
            'speed': False,
            'game_over': False
        }

        # score
        self.score_data = {
            'level': 1,
            'score': 0,
            'lines': 0
        }

        self.y_pos_score = [0, 0]

    def timer_update(self):
        """
        Update all timers
        """
        for timer in self.timers.values():
            timer.update_timer()

    def create_tetromino(self):
        """
        Create a new tetromino if game is not over.
        """
        # check if game is over
        self.check_game_over()

        # cancel speed up and reset timer to normal speed
        self.bools['speed'] = False
        self.timers['vertical'].duration = self.down_speed

        # calculate score if previous tetromino was sped up
        if pg.key.get_pressed()[pg.K_DOWN] and self.bools['down']:
            self.y_pos_score[1] = self.tetromino.get_y()
            self.score_data['score'] += self.y_pos_score[1] - self.y_pos_score[0]
        self.y_pos_score[0] = self.y_pos_score[1] = 0

        # check if lines have been filled
        self.check_full_lines()

        # spawn new tetromino
        if not self.bools['game_over']:
            self.tetromino = Tetromino(self.get_next(), self.sprite_group, self.create_tetromino, self.game_area)

    def move_down(self):
        """
        Calls move_down() from tetromino to move it down
        """
        self.tetromino.move_down()

    def check_full_lines(self):
        """
        Check for and clear full lines in the game area.
        This method iterates through each row in the game area, identifies full lines, clears them,
        shifts blocks above the cleared lines down, updates the game area, and calculates the score.
        """
        # list to store lines that need to be cleared
        clear_lines = []
        for i, line in enumerate(self.game_area):
            # check if all cells in the line are filled by blocks
            if all(line):
                clear_lines.append(i)

        if clear_lines:
            # clear the blocks in the identified lines
            for line in clear_lines:
                for block in self.game_area[line]:
                    block.kill()

                # shift blocks above the cleared lines down
                for row in self.game_area:
                    for block in row:
                        if block and block.pos.y < line:
                            block.pos.y += 1

            # update game area with the current state of the sprite group
            self.game_area = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
            for block in self.sprite_group:
                self.game_area[int(block.pos.y)][int(block.pos.x)] = block

            # calculate and update score based on the number of cleared lines
            self.calculate_score(len(clear_lines))

    def user_input(self):
        """
        Process user input.
        User can move tetromino left, right and down. He can also rotate the tetromino and drop it down.
        User can also pause and unpause the game using the escape key.
        """
        keys = pg.key.get_pressed()
        keys2 = pg.key.get_just_released()

        # left - right movement
        if not self.timers['horizontal'].active and not self.bools['paused'] and not self.bools['speed']:
            if keys[pg.K_LEFT]:
                self.tetromino.horizontal_move(-1)
                self.timers['horizontal'].activate()

            if keys[pg.K_RIGHT]:
                self.tetromino.horizontal_move(1)
                self.timers['horizontal'].activate()

        # rotation
        if not self.timers['rotation'].active and not self.bools['paused'] and not self.bools['speed']:
            if keys[pg.K_UP]:
                self.tetromino.rotate()
                self.timers['rotation'].activate()

        # speedup falling
        if not self.bools['down'] and not self.bools['paused'] and keys[pg.K_DOWN] and not self.bools['speed']:
            self.bools['down'] = True
            self.timers['vertical'].duration = self.down_speed_faster

            self.y_pos_score[0] = self.tetromino.get_y()

        if self.bools['down'] and not self.bools['paused'] and not keys[pg.K_DOWN] and not self.bools['speed']:
            self.bools['down'] = False
            self.timers['vertical'].duration = self.down_speed

            # add score for speeding up fall
            self.y_pos_score[1] = self.tetromino.get_y()
            self.score_data['score'] += self.y_pos_score[1] - self.y_pos_score[0]
            self.update_score(self.score_data['level'], self.score_data['score'], self.score_data['lines'])
            self.y_pos_score[0] = self.y_pos_score[1] = 0

        # instant fall
        if not self.bools['space'] and not self.bools['paused'] and keys[pg.K_SPACE] and not self.bools['speed'] and not self.bools['game_over']:
            self.bools['space'] = True
            self.bools['speed'] = True

            self.score_data['score'] += 2 * (20 - int(self.tetromino.blocks[0].pos.y))
            self.update_score(self.score_data['level'], self.score_data['score'], self.score_data['lines'])

            self.timers['vertical'].duration *= 0.1

        if self.bools['space'] and not self.bools['paused'] and not keys[pg.K_SPACE] and not self.bools['speed']:
            self.bools['space'] = False
            self.timers['vertical'].duration = self.down_speed

        # pause / unpause
        if self.bools['paused'] and not self.bools['game_over'] and not self.timers['vertical'].active and keys2[pg.K_ESCAPE]:
            # un-paused game
            self.bools['paused'] = False
            self.timers['vertical'].activate()
            self.timers['horizontal'].activate()
            self.timers['rotation'].activate()
            self.text_bg_colour = choice(list(COLOURS))
            return

        if not self.bools['paused'] and not self.bools['game_over'] and self.timers['vertical'].active and keys2[pg.K_ESCAPE]:
            # paused game
            self.bools['paused'] = True
            self.timers['vertical'].deactivate()
            self.timers['horizontal'].deactivate()
            self.timers['rotation'].deactivate()
            return

    def check_game_over(self):
        """
        Checks if player has failed and game is over
        """
        for block in self.tetromino.blocks:
            # check if a block is above game area
            if block.pos.y < 0:
                try:
                    # open high score file
                    with open('high_score.txt', 'r', encoding='utf8') as f:
                        tmp = f.read()
                        high_score = int(tmp) if tmp.isnumeric() else 0

                        # if current score is better than high score write new high score
                        if self.score_data['score'] > high_score:
                            with open('high_score.txt', 'w', encoding='utf-8') as output_file:
                                output_file.write(str(self.score_data['score']))
                except FileNotFoundError:
                    # if file has not been found create new file and write high score
                    with open('high_score.txt', 'w', encoding='utf-8') as f:
                        f.write(str(self.score_data['score']))

                # game is over
                self.bools['game_over'] = True

    def calculate_score(self, num_lines: int):
        """
        Calculates the score of the player
        :param num_lines: number of lines to add to score
        """
        # add lines to line count
        self.score_data['lines'] += num_lines

        # calculate score
        self.score_data['score'] += SCORE_POINTS[num_lines] * self.score_data['level']

        # for every 10 lines increase level and make game faster
        if self.score_data['lines'] // 10 > (self.score_data['lines'] - num_lines) // 10:
            self.score_data['level'] += 1
            self.down_speed *= 0.75
            self.down_speed_faster = SIDE_MOVE_DELAY
            self.timers['vertical'].duration = self.down_speed

        self.update_score(self.score_data['level'], self.score_data['score'], self.score_data['lines'])

    def render_grid(self):
        """
        Render game area grid
        """
        # draw lines in X axis
        for x in range(1, COLUMNS):
            pg.draw.line(self.surface, LINE_COLOUR, (x * CELL, 0), (x * CELL, self.surface.get_height()))

        # draw lines in Y axis
        for y in range(1, ROWS):
            pg.draw.line(self.surface, LINE_COLOUR, (0, y * CELL), (self.surface.get_width(), y * CELL))

        self.surface.blit(self.line, (0, 0))

    def pause_game_over_screen(self, texts: list[str], x_offset: list[int]):
        """
        Display given text on screen (either pause or game over)
        :param texts: list of texts to be rendered
        :param x_offset: int list containing x offset for given texts
        """
        self.surface.fill(BG_GAME_COLOUR)
        self.render_grid()

        # end screen text
        text_positions = [
            (self.surface.get_width() // 2, self.surface.get_height() // 2 - 150),
            (self.surface.get_width() // 2, self.surface.get_height() // 2 - 105)
        ]
        fonts = [self.fonts[0], self.fonts[1]]

        # render text and background
        for text, pos, font_1 in zip(texts, text_positions, fonts):
            text_surface = font_1.render(text, False, OUTLINE_COLOUR)
            text_rect = text_surface.get_rect(center=pos)

            # render text background with random colour
            background_rect = pg.Rect(text_rect.x - x_offset[0], text_rect.y, text_rect.width + x_offset[1],
                                      text_rect.height + 10)
            pg.draw.rect(self.surface, self.text_bg_colour, background_rect)

            self.surface.blit(text_surface, text_rect)

    def game_loop(self):
        """
        Loop of the game logic
        The loop continuously updates and renders the game components
        """
        self.user_input()
        self.timer_update()
        self.sprite_group.update()

        # rendering
        self.surface.fill(BG_GAME_COLOUR)
        self.sprite_group.draw(self.surface)
        self.render_grid()

        # render pause screen
        if self.bools['paused'] and not self.bools['game_over']:
            self.pause_game_over_screen(["Paused", "Press Escape to Continue"], [110, 210])

        # render game over screen
        if self.bools['game_over']:
            self.pause_game_over_screen(["Game Over", "Press Space to Restart"], [50, 100])

        self.screen.blit(self.surface, (PADDING * 2 + SIDEBAR_W, PADDING))
        pg.draw.rect(self.screen, OUTLINE_COLOUR, self.rect, 2, 5)
