import pymunk

from config import LEFT, RIGHT, TOP, BOTTOM

def create_static_boundaries(space: pymunk.Space) -> None:
    """Initializes the game boundary with static line segments"""

    static_body = space.static_body

    static_lines = [
        pymunk.Segment(static_body, (LEFT, TOP), (LEFT, BOTTOM), 5.0),
        pymunk.Segment(static_body, (RIGHT, TOP), (RIGHT, BOTTOM), 5.0),
        pymunk.Segment(static_body, (LEFT, TOP), (RIGHT, TOP), 5.0),
    ]
    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.9
    space.add(*static_lines)
