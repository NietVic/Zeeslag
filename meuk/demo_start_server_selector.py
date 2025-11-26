from guizero import *

# ---------------------------------------------------------
# NAVIGATIE FUNCTIES
# ---------------------------------------------------------

def show_start():
    server_select.hide()
    room_select.hide()
    ip_input.hide()
    start_screen.show()

def goto_server_select():
    start_screen.hide()
    room_select.hide()
    ip_input.hide()
    server_select.show()

def goto_room_select():
    server_select.hide()
    room_select.show()

def goto_ip_input():
    server_select.hide()
    ip_input.show()

def open_official_servers():
    goto_server_select()

def open_private_server():
    goto_ip_input()

def start_offline_game():
    print("Offline spel starten (demo)")

# ---------------------------------------------------------
# DEMO DATA
# ---------------------------------------------------------

official_servers = {
    "EU-West": ["Kamer 1", "Kamer 2", "Kamer 3"],
    "US-East": ["Room A", "Room B"],
    "Asia": ["Space K1", "Space K2", "Space K3", "Space K4"]
}

# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

app = App(title="Battleship Demo", width=800, height=600, layout="stack")

# ---------------------------------------------------------
# STARTSCHERM
# ---------------------------------------------------------

start_screen = Box(app, layout="stack")

# Achtergrond
background_pic = Picture(start_screen, image="bismarck.jpg", width=800, height=600)

# Voorgrond
start_fg = Box(start_screen, layout="grid")

# Titel
Text(start_fg, text="Battleship", grid=[0,0], size=20, color="white")

# Gebruikersnaam
Text(start_fg, text="Gebruikersnaam:", grid=[0,1], color="white")
username = TextBox(start_fg, grid=[0,2])

# Stijl voor blauwe knoppen (zodat het zichtbaar blijft boven de foto)
def styled_button(parent, text, grid, command=None):
    btn = PushButton(
        parent, 
        text=text, 
        grid=grid, 
        command=command, 
        width=20, 
        height=2#,
        text_color="white",
        border=3
    )
    # Border als blauwe knop
    btn.bg = "#1E3A8A"   # Donkerblauw
    return btn

styled_button(start_fg, "Officiële servers", [0,3], open_official_servers)
styled_button(start_fg, "Privéserver", [0,4], open_private_server)
styled_button(start_fg, "Offline spelen", [0,5], start_offline_game)

# ---------------------------------------------------------
# SERVER SELECTIE SCHERM
# ---------------------------------------------------------

server_select = Box(app, layout="grid", visible=False)
Text(server_select, text="Selecteer server", size=16, grid=[0,0,2,1])

Text(server_select, text="Officiële servers:", grid=[0,1])
server_list = ListBox(server_select, items=list(official_servers.keys()), grid=[0,2])

styled_button(server_select, "Ga naar ruimtes", [0,3], goto_room_select)

Text(server_select, text="Privéserver:", grid=[1,1])
styled_button(server_select, "Voer IP in", [1,2], goto_ip_input)

styled_button(server_select, "Terug", [0,4], show_start)

# ---------------------------------------------------------
# RUIMTE SELECTIE SCHERM
# ---------------------------------------------------------

room_select = Box(app, layout="grid", visible=False)

Text(room_select, text="Selecteer een ruimte", size=16, grid=[0,0])
room_list = ListBox(room_select, items=["(kies een server)"], grid=[0,1])

def room_select_show(event=None):
    sel = server_list.value
    if sel in official_servers:
        room_list.clear()
        for r in official_servers[sel]:
            room_list.append(r)

room_select.when_shown = room_select_show

styled_button(room_select, "Verbind", [0,2])
styled_button(room_select, "Terug", [0,3], goto_server_select)

# ---------------------------------------------------------
# PRIVÉSERVER IP-SCHERM
# ---------------------------------------------------------

ip_input = Box(app, layout="grid", visible=False)

Text(ip_input, text="Voer IP-adres in voor privéserver", size=16, grid=[0,0])
ip_box = TextBox(ip_input, grid=[0,1])

styled_button(ip_input, "Verbind", [0,2])
styled_button(ip_input, "Terug", [0,3], goto_server_select)

# ---------------------------------------------------------

app.display()
