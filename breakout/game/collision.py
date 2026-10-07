"""
collision: ball-vs-brick collision handling.
"""


def handle_ball_brick_collision(ball, brick):
    """Bounce the ball off a brick once and move it outside the brick."""

    ball_rect = ball.get_rect()
    brick_rect = brick.get_rect()

    if not ball_rect.colliderect(brick_rect):
        return False

    overlap_left = ball_rect.right - brick_rect.left
    overlap_right = brick_rect.right - ball_rect.left
    overlap_top = ball_rect.bottom - brick_rect.top
    overlap_bottom = brick_rect.bottom - ball_rect.top

    min_overlap = min(
        overlap_left,
        overlap_right,
        overlap_top,
        overlap_bottom,
    )

    if min_overlap == overlap_top:
        ball.y = brick_rect.top - ball.radius
        ball.vy = -abs(ball.vy)

    elif min_overlap == overlap_bottom:
        ball.y = brick_rect.bottom + ball.radius
        ball.vy = abs(ball.vy)

    elif min_overlap == overlap_left:
        ball.x = brick_rect.left - ball.radius
        ball.vx = -abs(ball.vx)

    else:
        ball.x = brick_rect.right + ball.radius
        ball.vx = abs(ball.vx)

    return True