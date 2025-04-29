from math import sqrt


def grid_to_world(q, r):
    tile_width = -2
    dx = sqrt(3)
    dy = tile_width - 1

    x = r * dx * 2 + (q % 2) * dx
    y = q * dy

    return x, y, 0