import pygame

from game.ball import Ball
from game.paddle import Paddle
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game import renderer


WIDTH = 800
HEIGHT = 600


class GameEngine:
    def __init__(self):
        self.lives = 3
        self.game_over = False

        self.score = 0
        self.multiplier = 1

        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30,
        )

        self._reset_ball()
        self.bricks = self._build_bricks()

    def _reset_ball(self):
        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT / 2,
            vx=4,
            vy=-4,
        )

    def _build_bricks(self):
        bricks = []

        for row in range(5):
            for col in range(10):
                x = 50 + col * 70
                y = 50 + row * 30

                if row == 0:
                    bricks.append(
                        Brick(
                            x=x,
                            y=y,
                            brick_type=Brick.UNBREAKABLE,
                            hits_remaining=-1,
                        )
                    )

                elif row == 1:
                    bricks.append(
                        Brick(
                            x=x,
                            y=y,
                            brick_type=Brick.STRONG,
                            hits_remaining=3,
                        )
                    )

                else:
                    bricks.append(
                        Brick(
                            x=x,
                            y=y,
                            brick_type=Brick.NORMAL,
                            hits_remaining=1,
                        )
                    )

        return bricks

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

    def _reset_game(self):
        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30,
        )

        self._reset_ball()
        self.bricks = self._build_bricks()

        self.lives = 3
        self.game_over = False

        self.score = 0
        self.multiplier = 1

    def update(self):
        if self.game_over:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if (
            self.ball.get_rect().colliderect(
                self.paddle.get_rect()
            )
            and self.ball.vy > 0
        ):
            self.ball.bounce_off_paddle(
                self.paddle.get_rect()
            )

        for brick in self.bricks:
            if handle_ball_brick_collision(
                self.ball,
                brick,
            ):
                destroyed = brick.hit()

                if destroyed:
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

                    self.bricks.remove(brick)

                break

        if self.ball.is_below(HEIGHT):
            self.lives -= 1

            self.multiplier = 1

            if self.lives > 0:
                self._reset_ball()

            else:
                self.game_over = True

    def draw(self, surface, font):
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