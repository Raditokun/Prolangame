import sys
import pygame
import random
from collections import deque #BFS 

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
PIPE_OFF = (220, 95, 95)
PIPE_ON = (255, 215, 75)



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
    "tpose":    (1, 1, 1, 0),
    "cross":    (1, 1, 1, 1),   
    "source":   (0, 1, 0, 0),
    "target":   (0, 0, 0, 1),
}

class Cell:
    def __init__(self, type=None, rots=0, locked=False):
        self.type = type #tipe pipe
        self.rots = rots #rotasinya
        self.locked = locked #bisa rotate?
        self.powered = False
    
    def connections(self):
        if self.type is None:
            return (0, 0, 0, 0)
        p = PATTERN[self.type]
        return tuple(p[(i - self.rots) % 4] for i in range(4))
    
    def rotate(self):
        if self.locked or self.type is None or self.type in ("source", "target"):
            return
        self.rots = (self.rots + 1) % 4
        print(f"Rotated cell to {self.rots * 90} degrees")


#grid = [[Cell()] * COLS] * ROWS  
grid = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]

#source target
grid[0][0].type = "source"
grid[0][0].rots = 1                
grid[ROWS - 1][COLS - 1].type = "target"
grid[ROWS - 1][COLS - 1].rots = 1    # open N 

def progate():
    for row in grid:
        for cell in row:
            cell.powered = False


    src = None 
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c].type == "source":
                src = (r,c)
                break
        if src:
            break
    if src is None:
        return
    
    grid[src[0]][src[1]].powered = True
    queue = deque([src])
    while queue:
        r, c = queue.popleft()
        conns = grid[r][c].connections()
        for d in range(4):
            if not conns[d]:
                continue                            # this side is closed
            dx, dy = DELTA[d]
            nr, nc = r + dy, c + dx
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue                            # off the board
            ncell = grid[nr][nc]
            if ncell.type is None or ncell.powered:
                continue                            
            if not ncell.connections()[(d + 2) % 4]:
                continue                            
            ncell.powered = True
            queue.append((nr, nc))


def is_won():
   
    for row in grid:
        for cell in row:
            if cell.type == "target":
                return cell.powered
    return False


#test
grid[2][1].type = "corner"      # bend N at column 1
grid[1][1].type = "corner"      # turn E at row 1
grid[1][2].type = "straight"    # straight across
grid[1][3].type = "straight"    # locked pivot
grid[1][3].rots = 1             # E-W (already in solution rot)
grid[1][3].locked = True
grid[1][4].type = "corner"      # bend S at column 4
grid[2][4].type = "corner"      # turn E at row 2

# distractors (not connected to the solution)
grid[3][2].type = "tpose"
grid[4][3].type = "cross"     


running = True
prev_won = False



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos #x,y mouse
            c = (mx - GRID_X) // CELL
            r = (my - GRID_Y) // CELL
            if 0 <= r < ROWS and 0 <= c < COLS: #dalem grid
                grid[r][c].rotate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # shuffle every rotatable pipe
            for row in grid:
                for cell in row:
                    if cell.type and cell.type not in ("source", "target") and not cell.locked:
                        cell.rots = random.randint(0, 3)

    progate()

    # win-state
    won = is_won()
    if won and not prev_won:
        print("CIRCUIT COMPLETE")
    elif not won and prev_won:
        print("circuit broken")
    prev_won = won

    screen.fill(BG_COLOR)
    #kotak grid
    panel_rect = pygame.Rect(
        GRID_X - PAD, GRID_Y - PAD,
        COLS * CELL + 2 * PAD, ROWS * CELL + 2 * PAD,
    )
    pygame.draw.rect(screen, PANEL_BG,   panel_rect, border_radius=14)
    pygame.draw.rect(screen, PANEL_EDGE, panel_rect, width=3, border_radius=14)

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


            arm_color = PIPE_ON if cell.powered else PIPE_OFF

            
            conns = cell.connections()
            for d in range(4):
                if conns[d]:
                    dx,dy = DELTA[d] #arah hadap
                    ex = cx + dx * (CELL // 2)
                    ey = cy + dy * (CELL // 2)
                    pygame.draw.line(screen, arm_color, (cx, cy), (ex, ey), 10)

            # overlay
            if cell.type == "source":
                pygame.draw.circle(screen, SOURCE_COLOR, (cx, cy), 22)
            elif cell.type == "target":
                ring_color = PIPE_ON if cell.powered else TARGET_COLOR
                pygame.draw.circle(screen, ring_color, (cx, cy), 22, width=4)
            else:
                pygame.draw.circle(screen, arm_color, (cx, cy), 12)   # hub glows with arms

            # locked-cell marker 
            if cell.locked and cell.type not in ("source", "target"):
                pygame.draw.circle(screen, (220, 95, 95), (cx, cy), 5)
               
    



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
