"""
Eenvoudig, niet-functioneel zeeslag-voorbeeld met guizero.
Opslaan als `zeeslag_guizero.py` en uitvoeren met: `python zeeslag_guizero.py`.

Gedrag:
- Links: jouw veld (water = blauw, schepen = grijs).
- Rechts: tegenstander (fog = lichtgrijs). Bij klikken:
    - Als er geen schip ligt: vakje wordt blauw (miss).
    - Als er wel een schip ligt: vakje wordt geel (hit).
    - Als alle vakjes van hetzelfde schip zijn geraakt: die vakjes worden zwart (sunk).

Dit is een visuele demo — geen spelregels (plaatsen, beurtwisseling, AI, etc.)
"""
from guizero import App, Box, PushButton, Text

# Configuratie
ROWS = 10
COLS = 10
CELL_SIZE = 1  # kleiner gemaakt zodat beide velden passen

# Kleuren
COLOR_WATER = "#1E90FF"      # blauw voor water
COLOR_SHIP = "#A9A9A9"       # grijs voor schepen op eigen veld
COLOR_FOG = "#D3D3D3"        # mistig lichtgrijs voor vijandelijk veld
COLOR_MISS = COLOR_WATER      # wordt blauw waar geschoten zonder schip
COLOR_HIT = "#FFD700"       # geel wanneer schip geraakt
COLOR_SUNK = "#000000"      # zwart wanneer een schip volledig is gezonken

OWN_SHIPS = [
    [(0,0),(0,1),(0,2)],
    [(4,5),(5,5),(6,5),(7,5)],
]
OPPONENT_SHIPS = [
    [(1,1),(1,2)],
    [(3,3),(3,4),(3,5)],
    [(6,0),(7,0),(8,0),(9,0)],
]

def ships_to_map(ships):
    d = {}
    for idx, ship in enumerate(ships):
        for (r,c) in ship:
            d[(r,c)] = idx
    return d

OWN_SHIP_MAP = ships_to_map(OWN_SHIPS)
OPP_SHIP_MAP = ships_to_map(OPPONENT_SHIPS)

own_buttons = [[None]*COLS for _ in range(ROWS)]
opp_buttons = [[None]*COLS for _ in range(ROWS)]
opp_hits = set()
opp_sunk_ships = set()

app = App(title="Zeeslag - visuele demo", width=900, height=450, layout="grid")

header = Text(app, text="Zeeslag (visuele demo) - Links: jouw veld | Rechts: tegenstander", grid=[0,0,2,1])

left_box = Box(app, layout="grid", grid=[0,1])
Text(left_box, text="Jouw veld", grid=[0,0, COLS, 1])
board_box_left = Box(left_box, layout="grid", grid=[0,1])

for r in range(ROWS):
    for c in range(COLS):
        bg = COLOR_SHIP if (r,c) in OWN_SHIP_MAP else COLOR_WATER
        btn = PushButton(board_box_left, text=" ", grid=[r,c], width=CELL_SIZE, height=CELL_SIZE)
        btn.tk.config(bg=bg, activebackground=bg, relief="raised")
        own_buttons[r][c] = btn

right_box = Box(app, layout="grid", grid=[1,1])
Text(right_box, text="Tegenstander (klik om te schieten)", grid=[0,0, COLS, 1])
board_box_right = Box(right_box, layout="grid", grid=[0,1])

def check_and_mark_sunk(ship_idx):
    ship = OPPONENT_SHIPS[ship_idx]
    for cell in ship:
        if cell not in opp_hits:
            return False
    opp_sunk_ships.add(ship_idx)
    for (r,c) in ship:
        btn = opp_buttons[r][c]
        btn.tk.config(bg=COLOR_SUNK, activebackground=COLOR_SUNK, relief="sunken")
    return True

def shoot(r, c):
    btn = opp_buttons[r][c]
    if (r,c) in opp_hits:
        return
    opp_hits.add((r,c))
    if (r,c) in OPP_SHIP_MAP:
        btn.tk.config(bg=COLOR_HIT, activebackground=COLOR_HIT, relief="sunken")
        ship_idx = OPP_SHIP_MAP[(r,c)]
        check_and_mark_sunk(ship_idx)
    else:
        btn.tk.config(bg=COLOR_MISS, activebackground=COLOR_MISS, relief="sunken")

for r in range(ROWS):
    for c in range(COLS):
        btn = PushButton(board_box_right, text=" ", grid=[r,c], width=CELL_SIZE, height=CELL_SIZE, command=lambda rr=r, cc=c: shoot(rr,cc))
        btn.tk.config(bg=COLOR_FOG, activebackground=COLOR_FOG)
        opp_buttons[r][c] = btn

Text(app, text="Legenda: Blauw = water / miss, Grijs = eigen schip, Geel = hit, Zwart = gezonken schip, Lichtgrijs = mist (onbekend)", grid=[0,2,2,1])

app.display()