import pygame
import sys

from maps import TILE_MAP, screen_to_grid, draw_map
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Iso starter — click to move")
    clock = pygame.time.Clock()

    cam_x, cam_y = 400 - 32, 100
    player = Player(3.0, 3.0)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                col, row = screen_to_grid(mx, my, cam_x, cam_y)
                if 0 <= row < len(TILE_MAP) and 0 <= col < len(TILE_MAP[0]):
                    player.set_target(col, row)

        keys = pygame.key.get_pressed()
        pan = 300 * dt
        if keys[pygame.K_LEFT]:  cam_x += pan
        if keys[pygame.K_RIGHT]: cam_x -= pan
        if keys[pygame.K_UP]:    cam_y += pan
        if keys[pygame.K_DOWN]:  cam_y -= pan

        player.update(dt)

        mx, my = pygame.mouse.get_pos()
        hover = screen_to_grid(mx, my, cam_x, cam_y)

        screen.fill((20, 20, 30))
        draw_map(screen, cam_x, cam_y, hover, (int(player.target_col), int(player.target_row)))
        player.draw(screen, cam_x, cam_y)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
