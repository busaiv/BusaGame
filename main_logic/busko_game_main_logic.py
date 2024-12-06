from models import creatures
from models import dungeon
import utils

class BuskoGame:
    def __init__(self):
        self.active_dungeon = None
        self.active_player = None
        self.current_room = None

    def __repr__(self):
        return self.active_dungeon

    def init_game(self, active_dungeon, active_player=creatures.Player(input('Enter your name: '),
                                                             10, 2, 10,
                                                             5, 0)):
        self.active_dungeon = dungeon.Dungeon(active_dungeon)
        self.active_dungeon.set_floors({1: [], 2: [], 3: [], 4: [], 5: []})
        self.active_player = active_player
        utils.fill_dungeon(self.active_dungeon)


    def start_game(self):
        return utils.welcome_message(self.active_dungeon, self.active_player)

    def main_game(self):
        return utils.main_logic(self.active_dungeon, self.active_player)

    def end_game(self):
        return utils.end_message(self.active_dungeon, self.active_player)


if __name__ == '__main__':
    game = BuskoGame()
    game.init_game('test_dungeon')
    print(game.active_dungeon)
    print(game.start_game())
    print(game.main_game())
    print(game.end_game())

    print(f'\nLEADERBOARD:')
    for i, j in enumerate(utils.show_leaderboard()):
        print(f'|place: {i + 1}| |name: {j[1]}| |score: {j[2]}|\n')