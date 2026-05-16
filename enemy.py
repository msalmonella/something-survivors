import pygame
from maps import grid_to_screen, TILE_W, TILE_H

ENEMY_SPEED = 1.5
ENEMY_MAX_HP = 3
CONTACT_DIST = 0.7   # tiles — close enough to hurt player
CONTACT_DMG = 1
CONTACT_COOLDOWN = 1.0


class Enemy:
    def __init__(self, col, row):
        self.col = float(col)
        self.row = float(row)
        self.hp = ENEMY_MAX_HP
        self.dead = False
        self.flash = 0.0
        self.dmg_timer = 0.0   # cooldown so we don't spam damage

    def update(self, dt, player):
        dx = player.col - self.col
        dy = player.row - self.row
        dist = (dx * dx + dy * dy) ** 0.5
        if dist > 0.05:
            step = ENEMY_SPEED * dt
            self.col += dx / dist * step
            self.row += dy / dist * step
        self.flash = max(0.0, self.flash - dt)
        self.dmg_timer = max(0.0, self.dmg_timer - dt)
        # deal damage to player on contact
        if dist <= CONTACT_DIST and self.dmg_timer <= 0:
            self.dmg_timer = CONTACT_COOLDOWN
            player.take_damage(CONTACT_DMG)

    def draw(self, surface, cam_x, cam_y, zoom=1.0):
        x, y = grid_to_screen(self.col, self.row, cam_x, cam_y, zoom)
        cx = int(x + TILE_W * zoom / 2)
        cy = int(y + TILE_H * zoom / 2)
        s = max(1.0, zoom)

        color = (255, 80, 80) if self.flash > 0 else (50, 170, 50)
        pygame.draw.ellipse(surface, (0, 0, 0),
                            (cx - int(10*s), cy - int(3*s), int(20*s), int(6*s)))
        pygame.draw.circle(surface, color,           (cx, cy - int(14*s)), int(8*s))
        pygame.draw.circle(surface, (180, 230, 160), (cx, cy - int(26*s)), int(6*s))

        # health bar
        bar_w = int(20 * s)
        bar_h = max(2, int(3 * s))
        bar_x = cx - bar_w // 2
        bar_y = cy - int(36 * s)
        fill = int(bar_w * self.hp / ENEMY_MAX_HP)
        pygame.draw.rect(surface, (180, 0, 0),   (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (60, 220, 60), (bar_x, bar_y, fill,  bar_h))
