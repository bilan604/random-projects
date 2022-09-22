from typing import Dict
from . import board
from . import ship


class AiPlayer(object):

    def __innit(self, ships: Dict[str, ship.Ship], board_info: board.Board):
        self.ships = ships
        self.board = board_info
        self.type_name = "Ai"
        self.placement_locations = []
        for i in range(self.board.num_rows):
            for j in range(self.board.num_cols):
                self.placement_locations.append([int(i), int(j)])
        self.firing_locations = []
        for i in range(self.board.num_rows):
            for j in range(self.board.num_cols):
                self.firing_locations.append([int(i), int(j)])