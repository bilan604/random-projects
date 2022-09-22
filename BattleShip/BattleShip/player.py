import random
from typing import Dict, List
import copy
from . import game_config, board, ship, orientation, ship_placement, move
from .firing_location_error import FiringLocationError
from . import HumanPlayer
from . import orientation
from . import RandomAi
from . import CheatingAi
from . import SearchDestroyAi


class Player(object):
    opponents: List["Player"]
    ships: Dict[str, ship.Ship]

    def __init__(self, player_num: int, config: game_config.GameConfig, other_players: List["Player"]) -> None:
        super().__init__()
        self.ships = copy.deepcopy(config.available_ships)
        self.board = board.Board(config)
        self.coords_with_ships = []  # all coords with a ship on it for the player
        self.opponents = other_players[:]  # a copy of other players
        self.name = 'No Name'
        self.type = RandomAi.RandomAi(self.ships, self.board) #becomes an Ai class if Ai is given
        self.type_letter = "H"
        self.player_number = player_num
        self.init_name_or_type(player_num, other_players)
        self.place_ships()
        self.move_counter = 0

        for opponent in other_players:
            opponent.add_opponent(self)

    def init_name_or_type(self, player_num: int, other_players: List["Player"]) -> None:
        while True:
            coms = str("'")
            get_type = input(f'Enter one of [{coms}Human{coms}, {coms}CheatingAi{coms}, {coms}SearchDestroyAi{coms},'
                             f' {coms}RandomAi{coms}] for Player {self.player_number}{coms}s type: ').lower()
            if get_type[0] == "h":
                self.name = input(f"Player {player_num} please enter your name: ")
                if self.name in other_players:
                    print(f'Someone is already using {self.name} for their name.\n'
                          f'Please choose another name.')
                else:
                    self.type = HumanPlayer.HumanPlayer(self.ships, self.board)
                    break
            elif get_type[0] == "r":  #random
                self.type = RandomAi.RandomAi(self.ships, self.board)
                self.type_letter = "R"
                self.name = f"Random Ai {self.player_number}"
                self.display_placement_board()
                break
            elif get_type[0] == "c": #cheating
                self.type = CheatingAi.CheatingAi(self.ships, self.board, self.opponents)
                self.type_letter = "C"
                self.name = f"Cheating Ai {self.player_number}"
                self.display_placement_board()
                break
            elif get_type[0] == "s": #searchdestroy
                self.type = SearchDestroyAi.SearchDestroyAi(self.ships, self.board)
                self.type_letter = "S"
                self.name = f"Search Destroy AI {self.player_number}"
                self.display_placement_board()
                break

    def add_opponent(self, opponent: "Player") -> None:
        self.opponents.append(opponent)

    def place_ships(self) -> None:
        if self.type_letter == "H":
            for ship_ in self.ships.values():
                self.display_placement_board()
                self.place_ship(ship_, "H")
            self.display_placement_board()
        else:
            for ship_ in self.ships.values():
                self.place_ship(ship_, "A")
                self.display_placement_board()

    def place_ship(self, ship_: ship.Ship, letter: str = "H") -> None:
        if letter == "H":
            while True:
                placement = self.get_ship_placement(ship_)
                try:
                    self.board.place_ship(placement)
                    for row in range(placement.row_start, placement.row_end + 1):
                        for col in range(placement.col_start, placement.col_end + 1):
                            self.coords_with_ships.append([row, col])
                except ValueError as e:
                    print(e)
                else:
                    return

        else: #is Ai
            is_ok = 0
            while is_ok <= 5:
                try:
                    placement = self.get_ship_placement(ship_)
                    self.board.place_ship(placement)
                    is_ok += 10
                except ValueError:
                    pass

            for row in range(placement.row_start, placement.row_end + 1):
                for col in range(placement.col_start, placement.col_end + 1):
                    self.coords_with_ships.append([row, col])  # not sure if row col is even in int

    def get_ship_placement(self, ship_: ship.Ship):
        ship_len = ship_.length
        if self.type_letter == "H":
            while True:
                try:
                    orientation_ = self.get_orientation(ship_)
                    start_row, start_col = self.get_start_coords(ship_)
                except ValueError as e:
                    print(e)
                else:
                    return ship_placement.ShipPlacement(ship_, orientation_, start_row, start_col)
        else:
            integer = random.choice([0, 1])  #this decides randomly horizontal or vertical
            if integer == 0:
                ori = orientation.Orientation.HORIZONTAL
            elif integer == 1:
                ori = orientation.Orientation.VERTICAL

            if ori == orientation.Orientation.HORIZONTAL:
                start_row = random.randint(0, self.board.num_rows-1)
                start_col = random.randint(0, self.board.num_cols -int(ship_len))
                return ship_placement.ShipPlacement(ship_, ori, start_row, start_col)
            if ori == orientation.Orientation.VERTICAL:
                start_row = random.randint(0, self.board.num_rows -int(ship_len))
                start_col = random.randint(0, self.board.num_cols - 1)
                return ship_placement.ShipPlacement(ship_, ori, start_row, start_col)

    def get_orientation(self, ship_: ship.Ship) -> orientation.Orientation:
        orientation_ = input(
            f'{self.name} enter horizontal or vertical for the orientation of {ship_.name} '
            f'which is {ship_.length} long: ')
        return orientation.Orientation.from_string(orientation_)

    def get_start_coords(self, ship_: ship.Ship):
        coords = input(f'{self.name}, enter the starting position for your {ship_.name} ship'
                       f' ,which is {ship_.length} long, in the form row, column: ')
        try:
            row, col = coords.split(',')
        except ValueError:
            raise ValueError(f'{coords} is not in the form x,y')
        try:
            row = int(row)
        except ValueError:
            raise ValueError(f'{row} is not a valid value for row.\n'
                             f'It should be an integer between 0 and {self.board.num_rows - 1}')
        try:
            col = int(col)
        except ValueError:
            raise ValueError(f'{col} is not a valid value for column.\n'
                             f'It should be an integer between 0 and {self.board.num_cols - 1}')
        return row, col

    def all_ships_sunk(self) -> bool:
        return all(ship_.health == 0 for ship_ in self.ships.values())

    def get_move(self, letter: str) -> move.Move:
        if letter == "H":
            while True:
                coordinates = str(input(f'{self.name}, enter the location you want to fire at in the form row, column: '))
                try:
                    firing_location = move.Move.from_str(self, coordinates)
                except ValueError as e:
                    print(e)
                    continue
                return firing_location
        elif letter == "R":
            coord = random.choice(self.type.firing_locations)
            coords = f"{coord[0]},{coord[1]}"
            self.type.firing_locations.remove([int(coord[0]), int(coord[1])])
            firing_location = move.Move.from_str(self, coords)
            return firing_location
        elif letter == "C":
            for i in range(self.board.num_rows):
                for j in range(self.board.num_cols):
                    if [i, j] in self.opponents[0].coords_with_ships:
                        self.type.firing_locations.append([int(i), int(j)])
            coord = self.type.firing_locations[self.move_counter]
            coords = f"{coord[0]},{coord[1]}"
            self.move_counter += 1
            firing_location = move.Move.from_str(self, coords)
            return firing_location
        elif letter == "S":
            if self.type.destroy == False:
                coord = random.choice(self.type.firing_locations)
                coords = f"{coord[0]},{coord[1]}"
                self.type.firing_locations.remove([int(coord[0]), int(coord[1])])
                firing_location = move.Move.from_str(self, coords)
                return firing_location

            elif self.type.destroy == True:
                coord = self.type.firing_list[self.type.firing_list_progress] #a list
                coords = f"{coord[0]},{coord[1]}"
                firing_location = move.Move.from_str(self, coords)
                if self.type.firing_list_progress == len(self.type.firing_list)-1:
                    self.type.destroy = False
                #self.type.firing_list_progress += 1
                return firing_location

    def fire_at(self, row: int, col: int) -> None:
        opponent = self.opponents[0]
        if not opponent.board.coords_in_bounds(row, col):
            #if self.type.type_name == "SearchDestroy":
            #  self.type.firing_list_progress += 1
            raise FiringLocationError(f'{row}, {col} '
                                      f'is not in bounds of our '
                                      f'{opponent.board.num_rows} X {opponent.board.num_cols} board.')
        elif opponent.board.has_been_fired_at(row, col):
            #if self.type.type_name == "SearchDestroy":
            #    self.type.firing_list_progress += 1
            raise FiringLocationError(f'You have already fired at {row}, {col}.')

        else:
            a = opponent.receive_fire_at(row, col)
            if a == True and self.type.type_name == "SearchDestroy":
                self.type.destroy = True
                #if col - 1 >= 0:
                self.type.firing_list.append([row, col - 1])
                #if row - 1 >= 0:
                self.type.firing_list.append([row-1, col])
                #if col + 1 < self.board.number_cols:
                self.type.firing_list.append([row, col + 1])
                #if row + 1 < self.board.number_rows:
                self.type.firing_list.append([row + 1, col])
            self.display_scanning_boards()
            self.display_firing_board()

    def receive_fire_at(self, row: int, col: int) -> bool:
        location_fired_at = self.board.shoot(row, col)
        if location_fired_at.contains_ship():
            ship_hit = self.ships[location_fired_at.content]
            ship_hit.damage()
            print(f"You hit {self.name}'s {ship_hit}!")
            if ship_hit.destroyed():
                print(f"You destroyed {self.name}'s {ship_hit}")
            return True
        else:
            print('Miss')
            return False


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        else:
            return self.name == other.name

    def __ne__(self, other: object) -> bool:
        return self != other

    def display_empty_board_at_start(self):
        print(self.get_visible_representation_of_board(), end='')

    def display_placement_board(self) -> None:
        print(f"{self.name}'s Placement Board")
        print(self.get_visible_representation_of_board(), end='')

    def display_scanning_boards(self) -> None:
        print(f"{self.name}'s Scanning Board")
        for opponent in self.opponents:
            print(opponent.get_hidden_representation_of_board(), end='')

    def display_firing_board(self) -> None:
        print(f"\n{self.name}'s Board")
        print(self.get_visible_representation_of_board())

    def get_hidden_representation_of_board(self) -> str:
        return self.board.get_display(hidden=True)

    def get_visible_representation_of_board(self) -> str:
        return self.board.get_display(hidden=False)

    def __str__(self) -> str:
        return self.name

