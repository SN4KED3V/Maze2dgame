import turtle
import math
import random

# ═══════════════════════════════════════════════════════════════
#  DUNGEON MAZE  –  Realistic Emoji Edition
#  Controls: Arrow Keys or WASD  |  R = Restart
# ═══════════════════════════════════════════════════════════════

screen = turtle.Screen()
screen.title("Find Your Way Home")
screen.bgcolor("#1a1209")
screen.setup(width=680, height=720)
screen.tracer(0)
try:
    screen.cv._rootwindow.resizable(False, False)
except Exception:
    pass

# ── Palette (all 6-digit hex only) ──────────────────────────────
C_STONE_DARK  = "#2c2416"
C_STONE_MID   = "#3d3020"
C_STONE_LIGHT = "#5a4830"
C_MORTAR      = "#1e1710"
C_FLOOR_DARK  = "#1c1508"
C_FLOOR_MID   = "#251c0e"
C_FLOOR_LIGHT = "#2e2310"
C_TEXT        = "#d4b896"
C_GOLD        = "#f5c518"
C_AMBER       = "#8a6a3a"
C_SHADOW      = "#111111"
C_TORCH_A     = "#ff6600"
C_TORCH_B     = "#cc4400"
C_TORCH_C     = "#ffaa00"
C_TORCH_D     = "#ff8800"
C_GOAL_A      = "#3a2800"
C_GOAL_B      = "#5a3d00"
C_WIN_BG      = "#1a1000"
C_WIN_BD      = "#c8960c"
C_FRAME_BD    = "#3d2e1a"
C_FRAME_BG    = "#110c05"

# ── Maze (15×15) ────────────────────────────────────────────────
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROWS, COLS   = len(MAZE), len(MAZE[0])
CELL         = 36
MX           = -COLS * CELL / 2
MY           =  ROWS * CELL / 2 + 10
PLAYER_START = (13, 1)
GOAL         = (1, 13)

def cell_xy(r, c):
    return MX + c * CELL + CELL / 2, MY - r * CELL - CELL / 2

# ── Generic turtle factory ───────────────────────────────────────
def new_pen():
    t = turtle.Turtle()
    t.hideturtle(); t.speed(0); t.penup()
    return t

# ── Draw a filled circle WITHOUT using .dot() ───────────────────
def draw_circle(pen, cx, cy, radius, color):
    pen.goto(cx, cy - radius)
    pen.setheading(0)
    pen.pendown()
    pen.fillcolor(color)
    pen.pencolor(color)
    pen.pensize(1)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()
    pen.penup()

# ── Draw a filled rectangle ──────────────────────────────────────
def fill_rect(pen, x, y, w, h, color, border=None, bsize=1):
    pen.goto(x, y)
    pen.setheading(0)
    pen.fillcolor(color)
    pen.pencolor(border if border else color)
    pen.pensize(bsize)
    pen.pendown()
    pen.begin_fill()
    pen.forward(w); pen.left(90)
    pen.forward(h); pen.left(90)
    pen.forward(w); pen.left(90)
    pen.forward(h); pen.left(90)
    pen.end_fill()
    pen.penup()

# ════════════════════════════════════════════════════════════════
#  MAZE WORLD  (static, drawn once)
# ════════════════════════════════════════════════════════════════
rng = random.Random(42)   # seeded RNG so textures are deterministic

bg_pen   = new_pen()
wall_pen = new_pen()

def draw_stone_block(x, y, w, h):
    shade = rng.choice([C_STONE_DARK, C_STONE_MID, C_STONE_MID, C_STONE_LIGHT])
    fill_rect(wall_pen, x, y, w, h, shade, C_MORTAR, 1)
    # highlight streak top-left
    wall_pen.pencolor("#6b5540"); wall_pen.pensize(1)
    wall_pen.goto(x + 2, y + h - 2); wall_pen.pendown()
    wall_pen.goto(x + w // 3, y + h - 2); wall_pen.penup()
    wall_pen.goto(x + 2, y + h - 4); wall_pen.pendown()
    wall_pen.goto(x + w // 4, y + h - 4); wall_pen.penup()
    # shadow streak bottom-right
    wall_pen.pencolor("#120e07"); wall_pen.pensize(1)
    wall_pen.goto(x + w - 2, y + 2); wall_pen.pendown()
    wall_pen.goto(x + w * 2 // 3, y + 2); wall_pen.penup()

def draw_floor_tile(x, y, w, h):
    shade = rng.choice([C_FLOOR_DARK, C_FLOOR_MID, C_FLOOR_LIGHT, C_FLOOR_MID])
    fill_rect(wall_pen, x, y, w, h, shade, C_MORTAR, 1)
    if rng.random() < 0.3:
        wall_pen.pencolor("#302010"); wall_pen.pensize(1)
        sx = x + rng.randint(3, w - 6)
        wall_pen.goto(sx, y + h // 3); wall_pen.pendown()
        wall_pen.goto(sx + rng.randint(2, 6), y + h * 2 // 3)
        wall_pen.penup()

def draw_maze_world():
    pw = COLS * CELL + 20
    ph = ROWS * CELL + 20
    fill_rect(bg_pen, MX - 10, MY - ROWS * CELL - 10,
              pw, ph, C_FRAME_BG, C_FRAME_BD, 3)
    for r in range(ROWS):
        for c in range(COLS):
            wx = MX + c * CELL
            wy = MY - r * CELL - CELL
            if MAZE[r][c] == 1:
                draw_stone_block(wx, wy, CELL, CELL)
            else:
                draw_floor_tile(wx, wy, CELL, CELL)

# ════════════════════════════════════════════════════════════════
#  TORCHES  (flickering, redrawn each frame)
# ════════════════════════════════════════════════════════════════
torch_rng = random.Random(7)
torch_positions = []
for _r in range(1, ROWS - 1):
    for _c in range(1, COLS - 1):
        if MAZE[_r][_c] == 1:
            adj = sum(1 for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
                      if 0 <= _r+dr < ROWS and 0 <= _c+dc < COLS
                      and MAZE[_r+dr][_c+dc] == 0)
            if adj >= 2 and torch_rng.random() < 0.18:
                torch_positions.append((_r, _c))

torch_pens = [new_pen() for _ in torch_positions]

def draw_torches(t):
    for i, (r, c) in enumerate(torch_positions):
        tx, ty = cell_xy(r, c)
        tp = torch_pens[i]
        tp.clear()
        alpha   = 0.6 + 0.4 * math.sin(t + i * 1.3)
        glow_r  = int(10 + 4 * alpha)
        outer_c = C_TORCH_A if alpha > 0.7 else C_TORCH_B
        inner_c = C_TORCH_C if alpha > 0.7 else C_TORCH_D
        draw_circle(tp, tx, ty + 4, glow_r,     outer_c)
        draw_circle(tp, tx, ty + 4, glow_r // 2, inner_c)
        tp.goto(tx - 7, ty - 4)
        tp.write("🔥", align="left", font=("Segoe UI Emoji", 9, "normal"))

# ════════════════════════════════════════════════════════════════
#  GOAL  🏠
# ════════════════════════════════════════════════════════════════
goal_pen = new_pen()

def draw_goal():
    gx, gy = cell_xy(*GOAL)
    draw_circle(goal_pen, gx, gy, 19, C_GOAL_A)
    draw_circle(goal_pen, gx, gy, 13, C_GOAL_B)
    goal_pen.goto(gx - 12, gy - 13)
    goal_pen.write("🏠", align="left", font=("Segoe UI Emoji", 18, "normal"))

# ════════════════════════════════════════════════════════════════
#  PLAYER  🧙  + shadow
# ════════════════════════════════════════════════════════════════
shadow_pen = new_pen()
player_pen = new_pen()
pr, pc     = PLAYER_START

def draw_player():
    px, py = cell_xy(pr, pc)
    shadow_pen.clear()
    draw_circle(shadow_pen, px + 3, py - 5, 11, C_SHADOW)
    player_pen.clear()
    player_pen.goto(px - 12, py - 13)
    player_pen.write("🧙", align="left", font=("Segoe UI Emoji", 18, "normal"))

# ════════════════════════════════════════════════════════════════
#  FOOTPRINT TRAIL  👣
# ════════════════════════════════════════════════════════════════
MAX_TRAIL   = 18
trail_queue = []
trail_pool  = [new_pen() for _ in range(MAX_TRAIL + 5)]
trail_idx   = [0]

def add_footprint(r, c):
    fx, fy = cell_xy(r, c)
    tp = trail_pool[trail_idx[0] % len(trail_pool)]
    trail_idx[0] += 1
    tp.clear()
    tp.goto(fx - 7, fy - 9)
    tp.write("👣", align="left", font=("Segoe UI Emoji", 8, "normal"))
    trail_queue.append(tp)
    if len(trail_queue) > MAX_TRAIL:
        trail_queue.pop(0).clear()

def clear_trail():
    for tp in trail_queue:
        tp.clear()
    trail_queue.clear()

# ════════════════════════════════════════════════════════════════
#  HUD
# ════════════════════════════════════════════════════════════════
hud_pen = new_pen()
moves   = [0]

def update_hud():
    hud_pen.clear()
    hud_pen.goto(0, MY + 32)
    hud_pen.pencolor(C_AMBER)
    hud_pen.write("── DUNGEON MAZE ──", align="center",
                  font=("Courier New", 12, "bold"))
    hud_pen.goto(-130, MY + 14)
    hud_pen.pencolor(C_TEXT)
    hud_pen.write(f"Steps: {moves[0]}", align="left",
                  font=("Courier New", 10, "normal"))
    if moves[0] < 5:
        hud_pen.goto(130, MY + 14)
        hud_pen.pencolor(C_AMBER)
        hud_pen.write("Arrow keys / WASD", align="right",
                      font=("Courier New", 8, "normal"))

# ════════════════════════════════════════════════════════════════
#  WIN SCREEN
# ════════════════════════════════════════════════════════════════
win_pen   = new_pen()
game_over = [False]

def show_win():
    cx = 0
    cy = MY - ROWS * CELL / 2 + 15
    bx, by, bw, bh = cx - 160, cy - 46, 320, 92
    fill_rect(win_pen, bx, by, bw, bh, C_WIN_BG, C_WIN_BD, 2)
    win_pen.goto(cx, cy + 22)
    win_pen.pencolor(C_GOLD)
    win_pen.write("Quest Complete!", align="center",
                  font=("Courier New", 14, "bold"))
    win_pen.goto(cx, cy + 2)
    win_pen.pencolor(C_TEXT)
    win_pen.write(f"You escaped in {moves[0]} steps", align="center",
                  font=("Courier New", 10, "normal"))
    win_pen.goto(cx, cy - 18)
    win_pen.pencolor(C_AMBER)
    win_pen.write("Press  R  to play again", align="center",
                  font=("Courier New", 9, "normal"))

# ════════════════════════════════════════════════════════════════
#  FLICKER LOOP
# ════════════════════════════════════════════════════════════════
flicker_t = [0.0]

def flicker_loop():
    if not game_over[0]:
        flicker_t[0] += 0.25
        draw_torches(flicker_t[0])
        screen.update()
    screen.ontimer(flicker_loop, 120)

# ════════════════════════════════════════════════════════════════
#  MOVEMENT
# ════════════════════════════════════════════════════════════════
def try_move(dr, dc):
    global pr, pc
    if game_over[0]:
        return
    nr, nc = pr + dr, pc + dc
    if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
        add_footprint(pr, pc)
        pr, pc = nr, nc
        moves[0] += 1
        draw_player()
        update_hud()
        screen.update()
        if (pr, pc) == GOAL:
            game_over[0] = True
            show_win()
            screen.update()

def restart():
    global pr, pc
    pr, pc = PLAYER_START
    moves[0] = 0
    game_over[0] = False
    clear_trail()
    win_pen.clear()
    draw_player()
    update_hud()
    screen.update()

# ── Key bindings ─────────────────────────────────────────────────
screen.listen()
for key, args in [
    ("Up",    (-1,  0)), ("Down",  ( 1, 0)),
    ("Left",  ( 0, -1)), ("Right", ( 0, 1)),
    ("w",     (-1,  0)), ("s",     ( 1, 0)),
    ("a",     ( 0, -1)), ("d",     ( 0, 1)),
]:
    screen.onkey(lambda a=args: try_move(*a), key)
screen.onkey(restart, "r")
screen.onkey(restart, "R")

# ════════════════════════════════════════════════════════════════
#  LAUNCH
# ════════════════════════════════════════════════════════════════
draw_maze_world()
draw_torches(0.0)
draw_goal()
draw_player()
update_hud()
screen.update()
flicker_loop()
turtle.done()    
