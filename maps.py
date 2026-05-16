import pygame

TILE_W = 128
TILE_H = 64

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
    0: (95, 165, 90),
    1: (140, 140, 150),
    2: (70, 120, 200),
}


def grid_to_screen(col, row, cam_x, cam_y, zoom=1.0):
    tw, th = TILE_W * zoom, TILE_H * zoom
    x = (col - row) * (tw / 2) + cam_x
    y = (col + row) * (th / 2) + cam_y
    return x, y


def screen_to_grid(px, py, cam_x, cam_y, zoom=1.0):
    tw, th = TILE_W * zoom, TILE_H * zoom
    px -= cam_x + tw / 2
    py -= cam_y + th / 2
    col = (px / (tw / 2) + py / (th / 2)) / 2
    row = (py / (th / 2) - px / (tw / 2)) / 2
    return int(col), int(row)


def draw_tile(surface, x, y, color, zoom=1.0, outline=(25, 25, 30)):
    tw, th = int(TILE_W * zoom), int(TILE_H * zoom)
    points = [
        (x + tw // 2, y),
        (x + tw,      y + th // 2),
        (x + tw // 2, y + th),
        (x,           y + th // 2),
    ]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, outline, points, 1)


def draw_map(surface, cam_x, cam_y, hover, target, zoom=1.0):
    for row, line in enumerate(TILE_MAP):
        for col, tile in enumerate(line):
            x, y = grid_to_screen(col, row, cam_x, cam_y, zoom)
            color = TILE_COLORS[tile]
            if (col, row) == target:
                color = (255, 230, 120)
            elif (col, row) == hover:
                color = tuple(min(255, c + 40) for c in color)
            draw_tile(surface, x, y, color, zoom)
