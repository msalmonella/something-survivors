import pygame

TILE_W = 64
TILE_H = 32

TILE_MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

TILE_COLORS = {
    0: (95, 165, 90),    # grass
    1: (140, 140, 150),  # stone
    2: (70, 120, 200),   # water
}


def grid_to_screen(col, row, cam_x, cam_y):
    x = (col - row) * (TILE_W / 2) + cam_x
    y = (col + row) * (TILE_H / 2) + cam_y
    return x, y


def screen_to_grid(px, py, cam_x, cam_y):
    px -= cam_x + TILE_W // 2
    py -= cam_y + TILE_H // 2
    col = (px / (TILE_W / 2) + py / (TILE_H / 2)) / 2
    row = (py / (TILE_H / 2) - px / (TILE_W / 2)) / 2
    return int(col), int(row)


def draw_tile(surface, x, y, color, outline=(25, 25, 30)):
    points = [
        (x + TILE_W // 2, y),
        (x + TILE_W,      y + TILE_H // 2),
        (x + TILE_W // 2, y + TILE_H),
        (x,               y + TILE_H // 2),
    ]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, outline, points, 1)


def draw_map(surface, cam_x, cam_y, hover, target):
    for row, line in enumerate(TILE_MAP):
        for col, tile in enumerate(line):
            x, y = grid_to_screen(col, row, cam_x, cam_y)
            color = TILE_COLORS[tile]
            if (col, row) == target:
                color = (255, 230, 120)
            elif (col, row) == hover:
                color = tuple(min(255, c + 40) for c in color)
            draw_tile(surface, x, y, color)
