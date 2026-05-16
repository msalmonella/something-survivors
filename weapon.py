import pygame
from maps import grid_to_screen, TILE_W, TILE_H


class Sword:
    SWING_DUR = 0.25

    def __init__(self):
        self.cooldown = 1.0
        self.range = 2.0
        self.damage = 1
        self.cooldown_timer = 0.0
        self.swing_timer = 0.0

    def apply_upgrade(self, kind):
        if kind == "range_up":
            self.range *= 1.5
        elif kind == "damage_up":
            self.damage *= 2
        elif kind == "attack_speed_up":
            self.cooldown = max(0.1, self.cooldown * 0.5)

    def update(self, dt, player, enemies):
        self.cooldown_timer -= dt
        self.swing_timer = max(0.0, self.swing_timer - dt)
        if self.cooldown_timer <= 0:
            self.cooldown_timer = self.cooldown
            self.swing_timer = self.SWING_DUR
            self._strike(player, enemies)

    def _strike(self, player, enemies):
        for e in enemies:
            dx = e.col - player.col
            dy = e.row - player.row
            if (dx * dx + dy * dy) ** 0.5 <= self.range:
                e.hp -= self.damage
                e.flash = 0.15
                if e.hp <= 0:
                    e.dead = True

    def draw(self, surface, player, cam_x, cam_y, zoom=1.0):
        if self.swing_timer <= 0:
            return
        x, y = grid_to_screen(player.col, player.row, cam_x, cam_y, zoom)
        cx = int(x + TILE_W * zoom / 2)
        cy = int(y + TILE_H * zoom / 2) - int(14 * zoom)
        px_r = int(self.range * TILE_W * zoom / 2)
        alpha = int(200 * (self.swing_timer / self.SWING_DUR))
        surf = pygame.Surface((px_r * 2 + 4, px_r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 240, 80, alpha),
                           (px_r + 2, px_r + 2), px_r, max(2, int(4 * zoom)))
        surface.blit(surf, (cx - px_r - 2, cy - px_r - 2))
