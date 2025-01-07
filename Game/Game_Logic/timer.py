"""
This is the timer module, it is responsible the in-game timers (fall speed, rotation, side to side movement)
"""

import pygame as pg


class Timer:
    """
    Class representing a timer.
    """
    def __init__(self, dur: int, repeat: bool = False, function: () = None):
        self.repeat = repeat
        self.function = function
        self.duration = dur

        self.start_time = 0
        self.active = False

    def activate(self):
        """
        Activate timer
        """
        self.active = True
        self.start_time = pg.time.get_ticks()

    def deactivate(self):
        """
        Deactivate timer
        """
        self.active = False
        self.start_time = 0

    def update_timer(self):
        """
        Update timer
        """
        cur_time = pg.time.get_ticks()
        if cur_time - self.start_time >= self.duration and self.active:
            if self.function is not None and self.start_time != 0:
                self.function()

            # reset timer
            self.deactivate()

            # repeat timer
            if self.repeat:
                self.activate()
