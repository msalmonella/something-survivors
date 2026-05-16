import random
import pygame
from maps import grid_to_screen, TILE_W, TILE_H

ITEM_TYPES = ["range_up", "damage_up", "attack_speed_up"]

ITEM_COLORS = {
    "range_up":        (255, 220, 50),
    "damage_up":       (255, 80,  80),
    "attack_speed_up": (80,  160, 255),
}

ITEM_LABELS = {
    "range_up":        "MENZIL",
    "damage_up":       "HASAR",
    "attack_speed_up": "HIZ",
}

DROP_CHANCE = 0.35


class Item:
    def __init__(self, col, row, kind):
        self.col = col
        self.row = row
        self.kind = kind
        self.collected = False
        self.bob = random.uniform(0, 6.28)  # phase offset for bobbing

    def draw(self, surface, cam_x, cam_y, zoom, time):
        x, y = grid_to_screen(self.col, self.row, cam_x, cam_y, zoom)
        cx = int(x + TILE_W * zoom / 2)
        cy = int(y + TILE_H * zoom / 2)
        s = max(1.0, zoom)
        bob = int(3 * s * __import__("math").sin(time * 4 + self.bob))
        color = ITEM_COLORS[self.kind]
        pygame.draw.circle(surface, (0, 0, 0),       (cx,     cy - int(10*s) + bob), int(7*s))
        pygame.draw.circle(surface, color,            (cx,     cy - int(10*s) + bob), int(6*s))
        pygame.draw.circle(surface, (255, 255, 255),  (cx,     cy - int(10*s) + bob), int(6*s), max(1, int(s)))


def maybe_drop(col, row):
    if random.random() < DROP_CHANCE:
        return Item(col, row, random.choice(ITEM_TYPES))
    return None
