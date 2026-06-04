import sys
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bangboo Minigame")
clock = pygame.time.Clock() #throttle fps
BG_COLOR = (30, 30, 30)

#grid 
COLS, ROWS = 6,5
CELL = 100 #100x100
PAD = 16
GRID_X = (WIDTH - (COLS * CELL + (COLS-1) * PAD)) // 2
GRID_Y = (HEIGHT - (ROWS * CELL + (ROWS-1) * PAD)) // 2

PANEL_BG = (20, 50, 60)
PANEL_EDGE = (45, 90, 105)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.fill(BG_COLOR)
    #kotak grid
    panel_rect = pygame.Rect(
        GRID_X - PAD, GRID_Y - PAD,
        COLS * CELL + 2 * PAD, ROWS * CELL + 2 * PAD,
    )
    pygame.draw.rect(screen, PANEL_BG,   panel_rect, border_radius=14)
    pygame.draw.rect(screen, PANEL_EDGE, panel_rect, width=3, border_radius=14)
        
    
    



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
