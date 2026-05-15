import pygame
from maps import grid_to_screen, TILE_W, TILE_H

SPEED = 3.0  # tiles per second


class Player:
    def __init__(self, col=3.0, row=3.0):
        self.col = col
        self.row = row
        self.target_col = col
        self.target_row = row

    def set_target(self, col, row):
        self.target_col = float(col)
        self.target_row = float(row)

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

    def draw(self, surface, cam_x, cam_y):
        x, y = grid_to_screen(self.col, self.row, cam_x, cam_y)
        cx = int(x + TILE_W / 2)
        cy = int(y + TILE_H / 2)
        pygame.draw.ellipse(surface, (0, 0, 0), (cx - 12, cy - 4, 24, 8))   # shadow
        pygame.draw.circle(surface, (200, 60, 60),   (cx, cy - 16), 9)      # body
        pygame.draw.circle(surface, (255, 210, 170), (cx, cy - 30), 7)      # head
