import itertools
from . import game_config, player
import sys
import random


class Game(object):

    def __init__(self, game_config_file: str, num_players: int = 2) -> None:
        super().__init__()
        random.seed(int(sys.argv[2]))
        self.game_config = game_config.GameConfig(game_config_file)
        self.players = []  #list of player classes
        self.player_turn = 0
        self.setup_players(num_players)

    def setup_players(self, num_players: int) -> None:
        for player_num in range(1, num_players + 1):
            self.players.append(player.Player(player_num, self.game_config, self.players)) #an int, game_config, and the empty list


    def play(self) -> None:
        active_player = self.players[0]
        for active_player in itertools.cycle(self.players):
            self.do_current_players_turn(active_player)
            if self.game_is_over():
                break
        print(f'{active_player} won the game!')

    def do_current_players_turn(self, cur_player: player.Player) -> None:
        self.display_gamestate(cur_player)
        while True:
            move = cur_player.get_move(cur_player.type_letter)
            move.make(cur_player, cur_player.type_letter)
            if move.ends_turn():
                break

    @property
    def num_players(self) -> int:
        return len(self.players)

    def get_active_player(self) -> player.Player:
        return self.players[self.player_turn]

    def game_is_over(self) -> bool:
        return any(player_.all_ships_sunk() for player_ in self.players)

    def display_gamestate(self, cur_player: player.Player) -> None:
        cur_player.display_scanning_boards()
        cur_player.display_firing_board()
