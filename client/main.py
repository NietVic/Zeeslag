# main.py - GUI voor Zeeslag met class-based structuur

from guizero import App, Box, PushButton, Text
from game import Game

# Kleuren
COLOR_WATER = "#1E90FF"
COLOR_SHIP  = "#A9A9A9"
COLOR_FOG   = "#D3D3D3"
COLOR_HIT   = "#FFD700"
COLOR_SUNK  = "#000000"

CELL_SIZE = 1
ROWS = 10
COLS = 10

game = Game()

own_buttons = [[None]*COLS for _ in range(ROWS)]
opp_buttons = [[None]*COLS for _ in range(ROWS)]

app = App(title="Zeeslag", width=900, height=450, layout="grid")

header = Text(app, text="Zeeslag", grid=[0,0,2,1])

# -------------------------
# Eigen bord
# -------------------------
left_box = Box(app, layout="grid", grid=[0,1])
Text(left_box, text="Jouw veld", grid=[0,0, COLS, 1])
board_box_left = Box(left_box, layout="grid", grid=[0,1])

for r in range(ROWS):
    for c in range(COLS):
        btn = PushButton(board_box_left, text=" ", grid=[r,c], width=CELL_SIZE, height=CELL_SIZE)
        btn.tk.config(bg=COLOR_WATER, activebackground=COLOR_WATER,
                      highlightbackground="#555555", highlightthickness=1)
        own_buttons[r][c] = btn

# -------------------------
# Vijandelijk bord
# -------------------------
right_box = Box(app, layout="grid", grid=[1,1])
Text(right_box, text="Tegenstander (klik om te schieten)", grid=[0,0, COLS, 1])
board_box_right = Box(right_box, layout="grid", grid=[0,1])

def shoot(r, c):
    btn = opp_buttons[r][c]

    result, ship_idx = game.enemy_board.register_shot(r, c)

    if result == "miss":
        btn.tk.config(bg=COLOR_WATER)
    elif result == "hit":
        btn.tk.config(bg=COLOR_HIT)
    elif result == "sunk":
        for (rr, cc) in game.enemy_board.ships[ship_idx].coordinates:
            opp_buttons[rr][cc].tk.config(bg=COLOR_SUNK)

for r in range(ROWS):
    for c in range(COLS):
        btn = PushButton(board_box_right, text=" ", grid=[r,c],
                         width=CELL_SIZE, height=CELL_SIZE,
                         command=lambda rr=r, cc=c: shoot(rr, cc))
        btn.tk.config(bg=COLOR_FOG, activebackground=COLOR_FOG)
        opp_buttons[r][c] = btn


Text(app, text="Legenda: Blauw = water/miss, Grijs = eigen schip, Geel = hit, Zwart = gezonken schip",
     grid=[0,2,2,1])

# ----------------------------------------------------------------------
#  NIEUWE, WERKENDE SCHEEPS-PLAATS LOGICA MET ROTATIE + PREVIEW
# ----------------------------------------------------------------------

PLACE_SIZES = [5,4,4,3,3,3,2,2,2,2]
current_place_index = 0
placing = True
placing_vertical = False

player_grid = [[None]*COLS for _ in range(ROWS)]
preview_cells = []

def clear_preview():
    for (r,c) in preview_cells:
        if player_grid[r][c] is None:
            own_buttons[r][c].tk.config(bg=COLOR_WATER,
                                        highlightbackground="#555555")
    preview_cells.clear()

def hover_preview(r, c):
    if not placing:
        return
    clear_preview()
    size = PLACE_SIZES[current_place_index]
    cells = []

    if placing_vertical:
        if r + size > ROWS:
            return
        for rr in range(r, r+size):
            cells.append((rr, c))
    else:
        if c + size > COLS:
            return
        for cc in range(c, c+size):
            cells.append((r, cc))

    for (rr, cc) in cells:
        if player_grid[rr][cc] is None:
            own_buttons[rr][cc].tk.config(bg="#90EE90",
                                          highlightbackground="#00AA00")
    preview_cells[:] = cells

def rotate():
    global placing_vertical
    placing_vertical = not placing_vertical
    print("Rotatie:", "VERTICAAL" if placing_vertical else "HORIZONTAAL")

def place_ship(r, c):
    global current_place_index, placing
    if not placing:
        return

    size = PLACE_SIZES[current_place_index]
    cells = []

    if placing_vertical:
        if r + size > ROWS:
            return
        for rr in range(r, r+size):
            if player_grid[rr][c] is not None:
                return
            cells.append((rr, c))
    else:
        if c + size > COLS:
            return
        for cc in range(c, c+size):
            if player_grid[r][cc] is not None:
                return
            cells.append((r, cc))

    for (rr, cc) in cells:
        own_buttons[rr][cc].tk.config(
            bg=COLOR_SHIP,
            highlightthickness=1,
            highlightbackground="#000000"
        )
        player_grid[rr][cc] = current_place_index

    current_place_index += 1
    clear_preview()

    if current_place_index >= len(PLACE_SIZES):
        placing = False
        print("Alle schepen geplaatst!")


rotate_btn = PushButton(app, text="Draai schip (R)", grid=[1,0], command=rotate)

# Bindings op eigen veld
for r in range(ROWS):
    for c in range(COLS):
        btn = own_buttons[r][c]
        btn.update_command(lambda rr=r, cc=c: place_ship(rr, cc))
        btn.tk.bind("<Enter>",  lambda e, rr=r, cc=c: hover_preview(rr, cc))
        btn.tk.bind("<Leave>",  lambda e: clear_preview())

app.display()
