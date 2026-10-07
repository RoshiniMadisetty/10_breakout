import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    WIDTH = 60
    HEIGHT = 20

    def __init__(
        self,
        x,
        y,
        brick_type=NORMAL,
        hits_remaining=1,
    ):
        self.x = x
        self.y = y
        self.brick_type = brick_type
        self.hits_remaining = hits_remaining

        if brick_type == self.NORMAL:
            self.color = (80, 180, 255)

        elif brick_type == self.STRONG:
            self.color = (255, 180, 60)

        elif brick_type == self.UNBREAKABLE:
            self.color = (150, 150, 150)

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.WIDTH,
            self.HEIGHT,
        )

    def hit(self):
        if self.brick_type == self.UNBREAKABLE:
            return False

        self.hits_remaining -= 1

        return self.hits_remaining <= 0