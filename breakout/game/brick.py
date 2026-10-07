"""
Brick: a single brick with a defined durability/type.
"""

import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    TYPE_COLORS = {
        NORMAL: (200, 90, 90),
        STRONG: (230, 170, 60),
        UNBREAKABLE: (100, 120, 220),
    }

    def __init__(
        self,
        x,
        y,
        width,
        height,
        brick_type=NORMAL,
        hits_remaining=None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        if hits_remaining is None:
            hits_remaining = {
                self.NORMAL: 1,
                self.STRONG: 3,
                self.UNBREAKABLE: None,
            }[brick_type]

        self.hits_remaining = hits_remaining
        self.color = self.TYPE_COLORS[brick_type]

    def hit(self):
        """Apply one hit and return True if destroyed."""

        if self.brick_type == self.UNBREAKABLE:
            return False

        self.hits_remaining -= 1

        return self.hits_remaining <= 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height,
        )