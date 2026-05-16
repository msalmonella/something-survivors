import math
import random
import pygame
import sys

from maps import TILE_MAP, TILE_W, TILE_H, screen_to_grid, draw_map
from player import Player, PLAYER_MAX_HP
from enemy import Enemy
from weapon import Sword
from item import Item, maybe_drop

SPAWN_INTERVAL = 2.0
SPAWN_DIST = 7.0
PICKUP_DIST = 0.9   # tiles


def _target_cam(player, sw, sh, zoom):
    tw, th = TILE_W * zoom, TILE_H * zoom
    cx = sw / 2 - (player.col - player.row) * (tw / 2) - tw / 2
    cy = sh / 2 - (player.col + player.row) * (th / 2) - th / 2
    return cx, cy


def _spawn(player):
    angle = random.uniform(0, 2 * math.pi)
    return Enemy(
        player.col + math.cos(angle) * SPAWN_DIST,
        player.row + math.sin(angle) * SPAWN_DIST,
    )


def _draw_hud(surface, font, player, sword, kills, sw, sh, hud_icons):
    hp_bar_img, skull_icon, heart_overlay = hud_icons

    # Health bar — asset only, clipped to current HP
    bar_w = hp_bar_img.get_width()
    bar_h = hp_bar_img.get_height()
    bx, by = 20, sh - bar_h - 20
    fill = max(0, int(bar_w * player.hp / player.max_hp))
    dim = hp_bar_img.copy()
    dim.set_alpha(60)
    surface.blit(dim, (bx, by))
    if fill > 0:
        surface.blit(hp_bar_img, (bx, by), (0, 0, fill, bar_h))
    surface.blit(heart_overlay, (bx, by))

    # Kill counter — skull icon + number
    surface.blit(skull_icon, (20, 20))
    kill_surf = font.render(str(kills), True, (255, 255, 255))
    ky = 20 + skull_icon.get_height() // 2 - kill_surf.get_height() // 2
    surface.blit(kill_surf, (20 + skull_icon.get_width() + 10, ky))

    # Sword stats
    stats = font.render(
        f"Menzil: {sword.range:.1f}  Hasar: {sword.damage}  Hiz: {1/sword.cooldown:.1f}/s",
        True, (200, 200, 200),
    )
    surface.blit(stats, (20, 55))


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_W, SCREEN_H = screen.get_size()
    pygame.display.set_caption("Something Survivors")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    hp_bar_img = pygame.transform.smoothscale(
        pygame.image.load("assets/health-bar.png").convert_alpha(), (480, 96)
    )
    skull_icon = pygame.transform.smoothscale(
        pygame.image.load("assets/kill-count-skull.png").convert_alpha(), (320, 320)
    )
    heart_overlay = pygame.transform.smoothscale(
        pygame.image.load("assets/health-bar-heart.png").convert_alpha(), (96, 96)
    )
    hud_icons = (hp_bar_img, skull_icon, heart_overlay)

    player = Player(3.0, 3.0)
    zoom = 1.0
    cam_x, cam_y = _target_cam(player, SCREEN_W, SCREEN_H, zoom)
    time_acc = 0.0

    enemies = []
    items = []
    sword = Sword()
    spawn_timer = SPAWN_INTERVAL
    kills = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        time_acc += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                zoom *= 1.1 ** event.y
                zoom = max(0.25, min(4.0, zoom))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                col, row = screen_to_grid(mx, my, cam_x, cam_y, zoom)
                if 0 <= row < len(TILE_MAP) and 0 <= col < len(TILE_MAP[0]):
                    player.set_target(col, row)

        player.update(dt)

        # Spawn enemies
        spawn_timer -= dt
        if spawn_timer <= 0:
            spawn_timer = SPAWN_INTERVAL
            enemies.append(_spawn(player))

        for e in enemies:
            e.update(dt, player)

        sword.update(dt, player, enemies)

        # Collect dead enemies, maybe drop items
        for e in enemies:
            if e.dead:
                kills += 1
                drop = maybe_drop(e.col, e.row)
                if drop:
                    items.append(drop)
        enemies = [e for e in enemies if not e.dead]

        # Item pickup
        for it in items:
            if it.collected:
                continue
            dx = player.col - it.col
            dy = player.row - it.row
            if (dx*dx + dy*dy) ** 0.5 <= PICKUP_DIST:
                it.collected = True
                sword.apply_upgrade(it.kind)
        items = [it for it in items if not it.collected]

        # Camera follow
        tx, ty = _target_cam(player, SCREEN_W, SCREEN_H, zoom)
        t = 1.0 - math.exp(-5.0 * dt)
        cam_x += (tx - cam_x) * t
        cam_y += (ty - cam_y) * t

        # Subtle shake
        shake_x = math.sin(time_acc * 7.3) * 1.2 + math.sin(time_acc * 13.7) * 0.6
        shake_y = math.sin(time_acc * 9.1) * 1.2 + math.sin(time_acc * 11.3) * 0.6
        draw_cx = cam_x + shake_x
        draw_cy = cam_y + shake_y

        mx, my = pygame.mouse.get_pos()
        hover = screen_to_grid(mx, my, cam_x, cam_y, zoom)

        screen.fill((20, 20, 30))
        draw_map(screen, draw_cx, draw_cy, hover,
                 (int(player.target_col), int(player.target_row)), zoom)

        for it in items:
            it.draw(screen, draw_cx, draw_cy, zoom, time_acc)

        for e in sorted(enemies, key=lambda e: e.col + e.row):
            e.draw(screen, draw_cx, draw_cy, zoom)

        sword.draw(screen, player, draw_cx, draw_cy, zoom)
        player.draw(screen, draw_cx, draw_cy, zoom)

        _draw_hud(screen, font, player, sword, kills, SCREEN_W, SCREEN_H, hud_icons)

        pygame.display.flip()

        if player.hp <= 0:
            # Game over — basit ekran
            go = font.render("GAME OVER  (ESC)", True, (255, 80, 80))
            screen.blit(go, (SCREEN_W // 2 - go.get_width() // 2,
                             SCREEN_H // 2 - go.get_height() // 2))
            pygame.display.flip()
            while True:
                ev = pygame.event.wait()
                if ev.type == pygame.QUIT or (
                    ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE
                ):
                    running = False
                    break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
