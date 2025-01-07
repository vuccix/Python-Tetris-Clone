"""
This is the settings module, it contains all the constants used in the Tetris game
"""

import pygame as pg


# game size
COLUMNS, ROWS = 10, 20
CELL = 45
GAME_W, GAME_H = COLUMNS * CELL, ROWS * CELL

# sidebar size
SIDEBAR_W = 200
PREVIEW_H = 0.6
SCORE_H = 0.4

# window
PADDING = 10
WINDOW_W = GAME_W + SIDEBAR_W * 2 + PADDING * 4
WINDOW_H = GAME_H + PADDING * 2

# points for clearing lines
SCORE_POINTS = {1: 100, 2: 300, 3: 500, 4: 800}

# game behaviour
TETROMINO_OFFSET_L = pg.Vector2(COLUMNS // 2, 0)  # center tetrominos to the right
TETROMINO_OFFSET_R = pg.Vector2(COLUMNS // 2 - 1, 0)  # center tetrominos to the left
MOVE_DOWN_SPEED = 500
SIDE_MOVE_DELAY = 120
ROTATE_DELAY = 200

# colours
YELLOW = '#f1c00d'
RED = '#cd0000'
BLUE = '#0f40bd'
GREEN = '#2ad117'
PURPLE = '#b318ba'
CYAN = '#19d7ff'
ORANGE = '#ff9100'
BG_COLOUR = '#1f1f1f'
BG_GAME_COLOUR = '#0a0a0a0a'
OUTLINE_COLOUR = '#ffffff'
LINE_COLOUR = '#555555'

COLOURS = [YELLOW, RED, BLUE, GREEN, PURPLE, CYAN, ORANGE]

# shapes
TETROMINOS = {
    'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'colour': CYAN, 'offset': TETROMINO_OFFSET_R},
    'J': {'shape': [(0, 0), (0, -1), (0, 1), (-1, 1)], 'colour': BLUE, 'offset': TETROMINO_OFFSET_L},
    'L': {'shape': [(0, 0), (0, -1), (0, 1), (1, 1)], 'colour': ORANGE, 'offset': TETROMINO_OFFSET_R},
    'O': {'shape': [(0, 0), (0, -1), (1, 0), (1, -1)], 'colour': YELLOW, 'offset': TETROMINO_OFFSET_R},
    'S': {'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'colour': GREEN, 'offset': TETROMINO_OFFSET_R},
    'Z': {'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'colour': RED, 'offset': TETROMINO_OFFSET_L},
    'T': {'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'colour': PURPLE, 'offset': TETROMINO_OFFSET_R},
}
