from typing import Dict
from . import board
from . import ship


class RandomAi(object):

    def __init__(self, ships: Dict[str, ship.Ship], board_info: board.Board):
        self.type_name = "RandomAi"
        self.ships = ships
        self.row = board_info.number_rows
        self.col = board_info.number_cols

        self.placement_locations = []
        for i in range(self.row):
            for j in range(self.col):
                self.placement_locations.append([int(i), int(j)])

        self.firing_locations = []
        for i in range(self.row):
            for j in range(self.col):
                self.firing_locations.append([int(i), int(j)])
