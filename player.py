import pygame
from maps import grid_to_screen, TILE_W, TILE_H

SPEED = 3.0
PLAYER_MAX_HP = 10


class Player:
    def __init__(self, col=3.0, row=3.0):
        self.col = col
        self.row = row
        self.target_col = col
        self.target_row = row
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP

    def set_target(self, col, row):
        self.target_col = float(col)
        self.target_row = float(row)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def update(self, dt):
        dx = self.target_col - self.col
        dy = self.target_row - self.row
        dist = (dx * dx + dy * dy) ** 0.5
        if dist > 0.001:
            step = SPEED * dt
            if step >= dist:
                self.col, self.row = self.target_col, self.target_row
            else:
                self.col += dx / dist * step
                self.row += dy / dist * step

    def draw(self, surface, cam_x, cam_y, zoom=1.0):
        x, y = grid_to_screen(self.col, self.row, cam_x, cam_y, zoom)
        cx = int(x + TILE_W * zoom / 2)
        cy = int(y + TILE_H * zoom / 2)
        r = max(1, zoom)
        pygame.draw.ellipse(surface, (0, 0, 0), (cx - int(12*r), cy - int(4*r), int(24*r), int(8*r)))
        pygame.draw.circle(surface, (200, 60, 60),   (cx, cy - int(16*r)), int(9*r))
        pygame.draw.circle(surface, (255, 210, 170), (cx, cy - int(30*r)), int(7*r))
