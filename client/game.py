from board import Board

class Game:
    def __init__(self):
        self.player_board = Board(ships=[
            [(0,0),(0,1),(0,2)],
            [(4,5),(5,5),(6,5),(7,5)]
        ])
        self.enemy_board = Board(ships=[
            [(1,1),(1,2)],
            [(3,3),(3,4),(3,5)],
            [(6,0),(7,0),(8,0),(9,0)]
        ])
