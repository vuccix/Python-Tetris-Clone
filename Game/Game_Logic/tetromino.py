"""
This is the tetromino module, it is responsible for representing the pieces used to play the Tetris game
"""

from os import path
from settings import pg, TETROMINOS, COLUMNS, ROWS, CELL


class Tetromino:
    """
    Class to represent a Tetromino in the game
    """
    def __init__(self, shape: str, sprite_group: pg.sprite.Group, create_tetromino, game_area: list[list]):
        self.block_pos = TETROMINOS[shape]['shape']
        self.colour = TETROMINOS[shape]['colour']
        self.offset = TETROMINOS[shape]['offset']
        self.create_tetromino = create_tetromino
        self.game_area = game_area
        self.shape = shape

        self.blocks = [Block(sprite_group, pos, self.colour, self.offset) for pos in self.block_pos]

    def wall_collision(self, side: int) -> bool:
        """
        Check if tetromino has collided with other tetrominos or walls
        :param side: which side hase tetromino moved (1 - right, -1 left)
        :return: true if tetromino has collided, otherwise false
        """
        collisions = [block.wall_collide(int(block.pos.x + side), self.game_area) for block in self.blocks]
        # if tetromino has collided return true
        if any(collisions):
            return True
        return False

    def floor_collision(self) -> bool:
        """
        Check if tetromino has collided with other tetrominos or the floor
        :return: true if tetromino has collided, otherwise false
        """
        collisions = [block.floor_collide(int(block.pos.y + 1), self.game_area) for block in self.blocks]
        # if tetromino has collided return true
        if any(collisions):
            return True
        return False

    def horizontal_move(self, side: int):
        """
        Move the tetromino horizontally
        :param side: which side should tetromino move (1 - right, -1 - left)
        :return:
        """
        if not self.wall_collision(side):
            for block in self.blocks:
                block.pos.x += side

    def get_y(self) -> int:
        """
        :return: the y position of the tetromino
        """
        return int(self.blocks[0].pos.y)

    def move_down(self):
        """
        Move the tetromino down on the Y axis
        """
        # if tetromino has not collided move down
        if not self.floor_collision():
            for block in self.blocks:
                block.pos.y += 1
        # if tetromino has collided update game_area and create new tetromino
        else:
            for block in self.blocks:
                self.game_area[int(block.pos.y)][int(block.pos.x)] = block
            self.create_tetromino()

    def rotate(self) -> bool:
        """
        Rotate the tetromino
        :return: true if tetromino has rotated, otherwise false
        """
        # rotate all shapes except square (O)
        if self.shape != 'O':
            pivot = self.blocks[0].pos
            new_pos = [block.rotate_block(pivot) for block in self.blocks]

            for pos in new_pos:
                # if rotation is outside game area don't rotate and return false
                if pos.x < 0 or pos.x >= COLUMNS:
                    return False

                # if tetromino is on ground return false
                if pos.y >= ROWS:
                    return False

                # if tetromino has collided with other tetrominos return false
                if self.game_area[int(pos.y)][int(pos.x)]:
                    return False

            # rotate tetromino and return true
            for i, block in enumerate(self.blocks):
                block.pos = new_pos[i]
            return True
        return False


class Block(pg.sprite.Sprite):
    """
    Class to represent a block in the Tetromino
    """
    def __init__(self, group: pg.sprite.Group, pos: tuple[int, int], colour: str, offset: pg.Vector2):
        super().__init__(group)

        # load sprite image
        sprite_image = pg.image.load(path.join('Assets', 'sprite.png')).convert_alpha()

        # convert hex to RGB
        hex_color = colour.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

        # multiply tetromino colour on sprite
        sprite_image.fill((rgb[0], rgb[1], rgb[2], 255), special_flags=pg.BLEND_RGBA_MULT)

        # resize sprite to match CELL size
        sprite_image = pg.transform.scale(sprite_image, (CELL, CELL))

        self.image = sprite_image
        self.pos = pg.Vector2(pos) + offset
        x = self.pos.x * CELL
        y = self.pos.y * CELL
        self.rect = self.image.get_rect(topleft=(x, y))

    def wall_collide(self, x: int, game_area: list[list]) -> bool:
        """
        Checks if the block has collided with a wall or other tetrominos
        :param x: x position of the block
        :param game_area: the game area
        :return: true if collided, otherwise false
        """
        if (not 0 <= x < COLUMNS) or (game_area[int(self.pos.y)][x]):
            return True
        return False

    def floor_collide(self, y: int, game_area: list[list]) -> bool:
        """
        Checks if the block has collided with the floor or other tetrominos
        :param y: y position of the block
        :param game_area: the game area
        :return: true if collided, otherwise false
        """
        if y >= ROWS or (y >= 0 and game_area[y][int(self.pos.x)]):
            return True
        return False

    def rotate_block(self, pivot: pg.Vector2) -> pg.Vector2:
        """
        Rotates the block around the pivot
        :param pivot: rotation pivot
        :return: new position of the block
        """
        distance = self.pos - pivot
        rotated = distance.rotate(90)
        return pivot + rotated

    def update(self):
        """
        Updates the block position
        """
        x = self.pos.x * CELL
        y = self.pos.y * CELL
        self.rect = self.image.get_rect(topleft=(x, y))
