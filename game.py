import sys
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bangboo Minigame")
clock = pygame.time.Clock() #throttle fps
BG_COLOR = (30, 30, 30) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(BG_COLOR)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
