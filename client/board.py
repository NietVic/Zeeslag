from ship import Ship

class Board:
    def __init__(self, rows=10, cols=10, ships=None):
        self.rows = rows
        self.cols = cols
        self.ships = [Ship(s) for s in ships] if ships else []

    def which_ship(self, r, c):
        for idx, ship in enumerate(self.ships):
            if ship.is_hit(r, c):
                return idx
        return None

    def register_shot(self, r, c):
        """Return: 'miss', 'hit', 'sunk', ship_index"""
        for idx, ship in enumerate(self.ships):
            if ship.is_hit(r, c):
                ship.register_hit(r, c)
                if ship.is_sunk():
                    return "sunk", idx
                return "hit", idx
        return "miss", None
