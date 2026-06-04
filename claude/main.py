"""Pipe Power - a minimal Pipe Mania / Netwalk core loop.

Inspired by the ZZZ rotating-node puzzle: align pipes from the yellow source
on the left to the target on the right. Powered segments glow yellow.

Controls:
    Left click  - rotate node 90 degrees clockwise
    R           - shuffle a new layout
    Esc / close - quit
"""

import sys
import random
from collections import deque
import pygame

pygame.init()

CELL = 90
COLS, ROWS = 6, 5
MARGIN = 40
HUD_H = 80
W = COLS * CELL + 2 * MARGIN
H = ROWS * CELL + 2 * MARGIN + HUD_H

BG = (12, 26, 36)
PANEL = (20, 50, 60)
GRID = (45, 90, 105)
OFF = (95, 175, 200)
ON = (255, 215, 75)
SRC = (255, 198, 45)
WIN_COL = (130, 240, 150)
DIM = (130, 160, 175)
LOCK = (220, 95, 95)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pipe Power")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("consolas", 32, bold=True)
status_font = pygame.font.SysFont("consolas", 18, bold=True)

# Connection patterns at rotation 0, ordered (N, E, S, W).
PATTERNS = {
    "straight": (1, 0, 1, 0),
    "corner":   (1, 1, 0, 0),
    "tee":      (1, 1, 1, 0),
    "source":   (0, 1, 0, 0),
    "target":   (0, 0, 0, 1),
}
DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))


class Cell:
    __slots__ = ("kind", "rot", "locked", "powered")

    def __init__(self, kind=None, rot=0, locked=False):
        self.kind = kind
        self.rot = rot
        self.locked = locked
        self.powered = False

    def conns(self):
        if not self.kind:
            return (0, 0, 0, 0)
        p = PATTERNS[self.kind]
        return tuple(p[(i - self.rot) % 4] for i in range(4))

    def rotate(self):
        if self.locked or not self.kind or self.kind in ("source", "target"):
            return False
        self.rot = (self.rot + 1) % 4
        return True


def make_level():
    g = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]
    layout = [
        (2, 0, "source",   0, False),
        (2, 1, "corner",   3, False),  # solution: N-W
        (1, 1, "corner",   1, False),  # solution: E-S
        (1, 2, "straight", 1, False),  # solution: E-W
        (1, 3, "corner",   2, True),   # locked pivot: S-W
        (2, 3, "corner",   0, False),  # solution: N-E
        (2, 4, "target",   0, False),
        (3, 4, "tee",      0, False),  # distractor
    ]
    for r, c, k, rot, lock in layout:
        g[r][c] = Cell(k, rot, lock)
    for row in g:
        for cell in row:
            if cell.kind and cell.kind not in ("source", "target") and not cell.locked:
                cell.rot = random.randint(0, 3)
    return g


def propagate(grid):
    for row in grid:
        for cell in row:
            cell.powered = False
    src = None
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c].kind == "source":
                src = (r, c)
                break
        if src:
            break
    if not src:
        return False
    grid[src[0]][src[1]].powered = True
    q = deque([src])
    while q:
        r, c = q.popleft()
        conns = grid[r][c].conns()
        for d, (dx, dy) in enumerate(DELTAS):
            if not conns[d]:
                continue
            nr, nc = r + dy, c + dx
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            ncell = grid[nr][nc]
            if not ncell.kind or ncell.powered:
                continue
            if not ncell.conns()[(d + 2) % 4]:
                continue
            ncell.powered = True
            q.append((nr, nc))
    for row in grid:
        for cell in row:
            if cell.kind == "target":
                return cell.powered
    return False


def draw_cell(r, c, cell):
    x = MARGIN + c * CELL
    y = HUD_H + MARGIN + r * CELL
    cx, cy = x + CELL // 2, y + CELL // 2
    pygame.draw.rect(screen, GRID, (x, y, CELL, CELL), 1)
    if not cell.kind:
        return
    color = ON if cell.powered else OFF
    for d, (dx, dy) in enumerate(DELTAS):
        if not cell.conns()[d]:
            continue
        ex = cx + dx * CELL // 2
        ey = cy + dy * CELL // 2
        pygame.draw.line(screen, color, (cx, cy), (ex, ey), 11)
    if cell.kind == "source":
        pygame.draw.circle(screen, SRC, (cx, cy), 24)
        pygame.draw.circle(screen, BG, (cx, cy), 24, 3)
        bolt = [(cx - 5, cy - 13), (cx + 3, cy - 2), (cx - 2, cy - 2), (cx + 5, cy + 13)]
        pygame.draw.lines(screen, BG, False, bolt, 3)
    elif cell.kind == "target":
        ring = color if cell.powered else OFF
        pygame.draw.circle(screen, ring, (cx, cy), 22, 4)
        pygame.draw.circle(screen, ring if cell.powered else PANEL, (cx, cy), 10)
    else:
        pygame.draw.circle(screen, color, (cx, cy), 15)
        pygame.draw.circle(screen, BG, (cx, cy), 15, 3)
        if cell.locked:
            pygame.draw.circle(screen, LOCK, (cx, cy), 6)


def draw(grid, won):
    screen.fill(BG)
    screen.blit(title_font.render("PIPE POWER", True, ON), (MARGIN, 15))
    if won:
        msg, col = "CIRCUIT COMPLETE  -  press R for a new layout", WIN_COL
    else:
        msg, col = "click a node to rotate  -  link source to target  -  R to shuffle", DIM
    screen.blit(status_font.render(msg, True, col), (MARGIN, 52))
    panel = pygame.Rect(MARGIN - 12, HUD_H + MARGIN - 12,
                        COLS * CELL + 24, ROWS * CELL + 24)
    pygame.draw.rect(screen, PANEL, panel, border_radius=14)
    pygame.draw.rect(screen, GRID, panel, 3, border_radius=14)
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(r, c, grid[r][c])
    pygame.display.flip()


def hit_test(pos):
    mx, my = pos
    if mx < MARGIN or my < HUD_H + MARGIN:
        return None
    c = (mx - MARGIN) // CELL
    r = (my - HUD_H - MARGIN) // CELL
    if 0 <= r < ROWS and 0 <= c < COLS:
        return r, c
    return None


def main():
    grid = make_level()
    won = propagate(grid)
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                hit = hit_test(ev.pos)
                if hit and grid[hit[0]][hit[1]].rotate():
                    won = propagate(grid)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    grid = make_level()
                    won = propagate(grid)
                elif ev.key == pygame.K_ESCAPE:
                    running = False
        draw(grid, won)
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
