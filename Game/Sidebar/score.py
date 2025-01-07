"""
This is the score module responsible for calculating and rendering the score
"""

from os import path
from settings import pg, SIDEBAR_W, GAME_H, SCORE_H, PADDING, WINDOW_H, OUTLINE_COLOUR, BG_GAME_COLOUR


class Score:
    """
    Class to represent the game score (point count, lines, level)
    """
    def __init__(self):
        self.surface = pg.Surface((SIDEBAR_W, GAME_H * SCORE_H - PADDING))
        self.rect = self.surface.get_rect(bottomleft=(PADDING, WINDOW_H - PADDING))
        self.display = pg.display.get_surface()

        self.surf_height = self.surface.get_height() // 3

        # initialize score, level and lines
        self.score_data = [1, 0, 0]  # level, score, lines

        # load font
        self.font = pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 25)

    def display_text(self, pos: tuple[float, float], text: tuple[str, int]):
        """
        Render the score on the screen
        :param pos: position where the text should be rendered
        :param text: text to be rendered
        """
        text_surface = self.font.render(f'{text[0]}\n{text[1]}', False, OUTLINE_COLOUR)
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def score_loop(self):
        """
        Score loop responsible for rendering the score
        """
        self.surface.fill(BG_GAME_COLOUR)
        for i, text in enumerate([('Score', self.score_data[1]), ('Level', self.score_data[0]), ('Lines',
                                                                                                 self.score_data[2])]):
            x = self.surface.get_width() / 3
            y = self.surf_height // 2 + i * self.surf_height
            self.display_text((x, y), text)

        self.display.blit(self.surface, self.rect)
        pg.draw.rect(self.display, OUTLINE_COLOUR, self.rect, 2, 5)
