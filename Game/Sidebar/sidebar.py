"""
This is the sidebar module, it's responsible for showing the list of next tetrominos to be spawned
"""

from os import path
from settings import (
    pg, SIDEBAR_W, GAME_H, PREVIEW_H, WINDOW_W, PADDING, TETROMINOS, BG_GAME_COLOUR, OUTLINE_COLOUR
)


class Sidebar:
    """
    Class to render the list of next shapes on the sidebar
    """
    def __init__(self):
        self.display = pg.display.get_surface()
        self.surface = pg.Surface((SIDEBAR_W, GAME_H * PREVIEW_H))
        self.rect = self.surface.get_rect(topright=(WINDOW_W - PADDING, PADDING))

        # load shape images
        self.shape_surf = {shape: pg.image.load(path.join('Assets', 'Next_Shape', f'{shape}.png')).convert_alpha() for
                           shape in TETROMINOS}

        # calculate surface height
        self.surf_height = self.surface.get_height() // 3

        # load font
        self.font = pg.font.Font(path.join('Assets', 'Silkscreen-Regular.ttf'), 25)

    def pieces(self, shapes: list[str]):
        """
        Render list of next tetromino pieces in the sidebar
        :param shapes: list of next tetromino pieces
        """
        for i, shape in enumerate(shapes):
            shape_surf = self.shape_surf[shape]

            # scale images to correct size
            if shape in ('J', 'L'):
                new_width = int(shape_surf.get_width() * 0.20)
                new_height = int(shape_surf.get_height() * 0.20)
            elif shape == 'I':
                new_width = int(shape_surf.get_width() * 0.25)
                new_height = int(shape_surf.get_height() * 0.25)
            else:
                new_width = int(shape_surf.get_width() * 0.15)
                new_height = int(shape_surf.get_height() * 0.15)

            shape_surf = pg.transform.scale(shape_surf, (new_width, new_height))

            # calculate correct position and render tetromino
            x = self.surface.get_width() // 2
            y = self.surf_height // 2 + i * self.surf_height
            rect = shape_surf.get_rect(center=(x, y + 20))
            self.surface.blit(shape_surf, rect)

    def sidebar_loop(self, next_shape: list[str]):
        """
        Sidebar loop responsible for rendering the sidebar
        :param next_shape: list of next tetromino shapes
        """
        self.surface.fill(BG_GAME_COLOUR)

        # write text
        text_surface = self.font.render("Next", False, OUTLINE_COLOUR)
        text_rect = text_surface.get_rect(midtop=(self.surface.get_width() // 2, 10))
        self.surface.blit(text_surface, text_rect)

        # show next 3 pieces
        self.pieces(next_shape)
        self.display.blit(self.surface, self.rect)
        pg.draw.rect(self.display, OUTLINE_COLOUR, self.rect, 2, 5)
