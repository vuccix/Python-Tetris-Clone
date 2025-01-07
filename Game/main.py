"""
This is the main module of the Tetris game responsible for running and rendering the whole application
"""
import sys
from random import choice
from os import path

# components
from settings import pg, WINDOW_W, WINDOW_H, TETROMINOS, SIDEBAR_W, PADDING, BG_COLOUR, OUTLINE_COLOUR
from Game_Logic.game import Game
from Sidebar.score import Score
from Sidebar.sidebar import Sidebar


class App:
    """
    The main application class for the Tetris game.
    This class initializes the game, manages the game loop, and renders all components
    """
    def __init__(self):
        """
        Initialize the game application
        This method sets up the game window, initializes components, and loads assets
        """
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pg.time.Clock()
        pg.display.set_caption('Pygame Tetris Clone')

        # initialize next shape list
        self.next_shape = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # initialize components
        self.components = {
            'game': Game(self.get_next, self.update_score),
            'score': Score(),
            'sidebar': Sidebar()
        }

        # load and scale controls image
        self.controls_image = pg.image.load(path.join('Assets', 'Controls.png')).convert_alpha()
        self.controls_image = pg.transform.scale(self.controls_image, (SIDEBAR_W, SIDEBAR_W))

        # load fonts
        self.fonts = {
            'default': pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 25),
            'logo': pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 55),
            'name': pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 19)
        }

        self.high_score = self.read_high_score()

    def get_next(self) -> str:
        """
        Get next tetromino in the sequence
        :return: str: The next tetromino from self.next_shape
        """
        next_shape = self.next_shape.pop(0)
        self.next_shape.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def update_score(self, level: int, score: int, lines: int):
        """
        Update score, lines and levels
        :param lines: int number of lines cleared
        :param score: int number of current score
        :param level: int number of current level
        """
        self.components['score'].score_data[0] = level
        self.components['score'].score_data[1] = score
        self.components['score'].score_data[2] = lines

    def render_controls(self):
        """
        Render controls image in the bottom right corner of the window
        """
        controls_text = self.fonts['default'].render("Controls", False, OUTLINE_COLOUR)
        controls_text_rect = controls_text.get_rect(
            midbottom=(WINDOW_W - PADDING - SIDEBAR_W // 2, WINDOW_H - PADDING - self.controls_image.get_height() - 10))
        self.screen.blit(controls_text, controls_text_rect)

        controls_rect = self.controls_image.get_rect(bottomright=(WINDOW_W - PADDING, WINDOW_H - PADDING))
        self.screen.blit(self.controls_image, controls_rect)

    def read_high_score(self) -> str:
        """
        Read high score from file
        :return: str: High score string or n/a if file not found
        """
        try:
            with open('high_score.txt', 'r', encoding='utf-8') as f:
                high_score = f.read()
                if high_score == '' or not high_score.isnumeric():
                    high_score = '0'
            return high_score
        except FileNotFoundError:
            return '0'

    def render_logo(self):
        """
        Render logo, my name and the high score
        """
        texts = ["Tetris", "skibidi", f"High Score\n{self.high_score}"]
        text_positions = [(PADDING - 5, PADDING), (PADDING, PADDING + 60), (PADDING, PADDING + 250)]
        fonts = [self.fonts['logo'], self.fonts['name'], self.fonts['default']]

        for text, pos, font in zip(texts, text_positions, fonts):
            text_surface = font.render(text, False, OUTLINE_COLOUR)
            text_rect = text_surface.get_rect(topleft=pos)
            self.screen.blit(text_surface, text_rect)

    def main_game_loop(self):
        """
        Run the main game loop
        The game loop continuously updates and renders the app components until the user exits
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill(BG_COLOUR)

            # render game
            self.components['game'].game_loop()
            self.components['score'].score_loop()
            self.components['sidebar'].sidebar_loop(self.next_shape)

            # render controls
            self.render_controls()

            # render logo
            self.render_logo()

            # restart game after game over
            if self.components['game'].bools['game_over'] and pg.key.get_just_released()[pg.K_SPACE]:
                # reinitialize values
                self.next_shape = [choice(list(TETROMINOS.keys())) for shape in range(3)]
                self.components['game'] = Game(self.get_next, self.update_score)
                self.components['score'] = Score()
                self.components['sidebar'] = Sidebar()
                self.high_score = self.read_high_score()

            # game tick
            pg.display.update()
            self.clock.tick()


if __name__ == "__main__":
    app = App()
    app.main_game_loop()
