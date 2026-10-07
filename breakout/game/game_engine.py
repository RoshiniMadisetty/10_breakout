"""
GameEngine: owns the paddle, ball, and bricks.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50


class GameEngine:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.multiplier = 1
        self.game_over = False

        self._reset_game()

    def _build_bricks(self):
        bricks = []

        total_width = (
            BRICK_COLS * (BRICK_WIDTH + BRICK_GAP)
            - BRICK_GAP
        )

        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (
                    BRICK_HEIGHT + BRICK_GAP
                )

                if row == 0:
                    brick_type = Brick.NORMAL

                elif row == 1:
                    brick_type = Brick.STRONG

                elif row == 2:
                    brick_type = Brick.UNBREAKABLE

                else:
                    brick_type = (
                        Brick.STRONG
                        if col % 2 == 0
                        else Brick.NORMAL
                    )

                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT,
                        brick_type,
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50,
        )

    def _reset_game(self):
        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30,
        )

        self._reset_ball()
        self.bricks = self._build_bricks()

        self.lives = 3
        self.score = 0
        self.multiplier = 1
        self.game_over = False

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self._reset_game()

    def update(self):
        if self.game_over:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        paddle_rect = self.paddle.get_rect()
        ball_rect = self.ball.get_rect()

        if (
            self.ball.vy > 0
            and ball_rect.colliderect(paddle_rect)
        ):
            self.ball.bounce_off_paddle(paddle_rect)

        for brick in self.bricks:
            if handle_ball_brick_collision(
                self.ball,
                brick,
            ):
                if brick.hit():
                    self.bricks.remove(brick)

                    if brick.brick_type == Brick.NORMAL:
                        points = 100

                    elif brick.brick_type == Brick.STRONG:
                        points = 200

                    else:
                        points = 0

                    if points > 0:
                        self.score += (
                            points * self.multiplier
                        )
                        self.multiplier += 1

                break

        if self.ball.is_below(HEIGHT):
            self.lives -= 1

            self.multiplier = 1

            if self.lives > 0:
                self._reset_ball()
            else:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.paddle,
            self.ball,
            self.bricks,
        )

        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35),
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 60),
        )

        renderer.draw_text(
            surface,
            font,
            f"Multiplier: x{self.multiplier}",
            (10, 85),
        )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                "GAME OVER - Press R to Restart",
            )