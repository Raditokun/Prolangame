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
SOURCE_COLOR = (255, 198, 45)
TARGET_COLOR = (130, 240, 150)


#arah hadap
N , E , S, W = 0,1,2,3


#x,y
#Semakin ke atas, semakin turun nilainya 
DELTA = (
    (0, -1), #North
    (1, 0),  #East
    (0, 1),  #South
    (-1, 0), #West
)

PATTERN = {
    "straight": (1, 0, 1, 0),
    "corner":   (1, 1, 0, 0),
    "tpose":      (1, 1, 1, 0),
    "source":   (0, 1, 0, 0),
    "target":   (0, 0, 0, 1),
}

class Cell:
    def __init__(self, type=None, rots=0, locked=False):
        self.type = type #tipe pipe
        self.rots = rots #rotasinya
        self.locked = locked #bisa rotate?
        self.powered = False


#grid = [[Cell()] * COLS] * ROWS  
grid = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]
grid[2][0].type = "source"
grid[2][COLS - 1].type = "target"

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

    #gambar gridlayout
    for r in range(ROWS):
        for c in range(COLS):
          
            

            cell_rect = pygame.Rect(GRID_X + c * CELL, GRID_Y + r * CELL, CELL, CELL)
            pygame.draw.rect(screen, PANEL_EDGE, cell_rect, width=1)


    for r in range(ROWS):
     for c in range(COLS):
            cell = grid[r][c]
            if cell.type is None:
                continue
            cx = GRID_X + c * CELL + CELL // 2
            cy = GRID_Y + r * CELL + CELL // 2

            if cell.type == "source":
                pygame.draw.circle(screen, SOURCE_COLOR, (cx, cy), 22)
            elif cell.type == "target":
                pygame.draw.circle(screen, TARGET_COLOR, (cx, cy), 22, width=4)
    



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
