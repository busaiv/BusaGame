from models.dungeon import Room
from models.objects import Weapon, Potion, Treasure, Object
from models.creatures import Player, Enemy
import sqlite3 # TODO: realize a saving\loading system
import random
import itertools

def rest_logic(player):
    def rest_result_yes(player_rst_yes):
        user_input = input(f'\nHere is your health: {player_rst_yes.health}\n'
                           f'Your inventory: {player_rst_yes.inventory}\n'
                           f'Do you want to heal? (y/n): ')
        if user_input == 'y':
            if len(player_rst_yes.inventory['potion']) > 0:
                potion = player_rst_yes.inventory['potion'].pop(0)
                potion.use(player_rst_yes)
                return rest_result_yes(player_rst_yes)
            else:
                return ('\nYou have no potions in your inventory'
                        '\nGet ready for the next action')
        else:
            return '\nGet ready for the next action'

    def main(player_rest):
        user_input = input('\nYou clear the whole room.\n'
                           'Do you want to rest? (y/n): ')
        if user_input == 'y':
            return rest_result_yes(player_rest)
        else:
            return '\nGet ready for the next action'

    print(main(player)) # TODO: print is not ok

def floor_info_logic(player, floor, floor_number):
    def insert_player(player_ins, floor_ins):
        floor_ins.insert(0, player_ins)

    def main(player_flr, floor_flr, floor_number_flr):
        if floor_flr[0] is not player:
            insert_player(player_flr, floor_flr)
            return (f'\nYou reached the end of the {floor_number_flr - 1} floor\n'
                    f'And get to the {floor_number_flr} floor')
        else:
            return f'You are on the {floor_number_flr} floor\n'

    print(main(player, floor, floor_number)) # TODO: print is not ok


def dead_kill_logic(player, enemy, room): # TODO: not useful for now
    if player.health <= 0:
        return f'You are dead'
    elif enemy.health <= 0:
        room.remove_object(enemy)
        return f'You killed the {enemy.name}'


def inventory_logic(player, item, room):
    def take_item(player_itm, item_itm, room_itm):
        if isinstance(item_itm, Potion):
            player_itm.take_potion(room_itm.remove_object(item_itm))
        elif isinstance(item_itm, Treasure):
            trs = room_itm.remove_object(item_itm)
            player_itm.add_points(trs.get_value())
            player_itm.take_treasure(trs)
        return (f'\nYou picked up {item_itm.name}\n'
                f'Your inventory: {player_itm.inventory}')

    def equip_weapon(player_wpn, item_wpn, room_wpn):
        player_wpn.equip_weapon(room_wpn.remove_object(item_wpn))
        return (f'\nYou equipped {item_wpn.name}\n'
                f'Your weapon: {player_wpn.weapon}\n'
                f'Your inventory: {player_wpn.inventory}')

    def main(player_inv, item_inv, room_inv):
        if isinstance(item_inv, Weapon):
            return equip_weapon(player_inv, item_inv, room_inv)
        else:
            return take_item(player_inv, item_inv, room_inv)

    print(main(player, item, room)) # TODO: print is not ok


def stealth_logic(player, enemy):
    def stealth_result_no(player_rst, enemy_rst):
        damage = enemy_rst.attack(player_rst)
        return (f'The {enemy_rst} sees you and hits you for {damage} damage\n'
                f'There is no way to avoid a fight.\n'
                f'Your health: {player_rst.health}\n'
                f'Enemy health: {enemy_rst.health}\n')

    def stealth_result_yes(player_rst, enemy_rst):
        stealth_roll = random.randint(1, 20)
        if stealth_roll >= enemy_rst.alertness:
            user_input = input(f'\nYou successfully sneak past the {enemy_rst.name}.\n'
                               f'Do you want to stealth attack? (y/n): ')
            if user_input == 'y':
                damage = player_rst.stealth_attack(enemy_rst)
                if enemy_rst.health <= 0:
                    player_rst.add_points(enemy_rst.get_value())
                    return f'\nYou killed the {enemy_rst.name} with stealth attack'
                return (f'\nYou hit the {enemy_rst.name} for {damage} damage\n'
                        f'Get ready for the fight!\n'
                        f'Your health: {player_rst.health}\n'
                        f'Enemy health: {enemy_rst.health}\n')
            else:
                enemy_rst.set_key(False)
                enemy_rst.hit(1000000)
                return '\nYou avoided the fight\n'
        else:
            damage = enemy_rst.attack(player_rst)
            return (f'You failed to sneak past the {enemy_rst.name}\n'
                    f'There is no way to avoid a fight.\n\n'
                    f'{enemy_rst.name} hit you for {damage} damage\n'
                    f'Your health: {player_rst.health}\n'
                    f'Enemy health: {enemy_rst.health}')

    def main(player_stl, enemy_stl):
        user_input = input(f'You need to roll a dice\n'
                           f'Roll? (y/n): ')
        if user_input == 'y':
            return stealth_result_yes(player_stl, enemy_stl)
        elif user_input == 'n':
            return stealth_result_no(player_stl, enemy_stl)

    print(main(player, enemy)) # TODO: print is not ok


def battle_logic(player, enemy):
    while player.health > 0 and enemy.health > 0:
        def player_roll(player_rll, enemy_rll):
            if player_rll.health <= 0:
                return '\nYou are dead'
            if enemy_rll.health <= 0:
                player_rll.add_points(enemy_rll.get_value())
                print('plrll')
                return f'\nYou killed the {enemy_rll.name}'
            roll = random.randint(1, 20)
            if roll > enemy_rll.armor:
                damage = player_rll.attack(enemy)
                return (f'\nGood job, you hit the {enemy_rll.name} for {damage} damage\n'
                        f'Your health: {player_rll.health}\n'
                        f'{enemy_rll.name} health: {enemy_rll.health}')
            else:
                return (f'\nYou miss!\n'
                        f'Your health: {player_rll.health}\n'
                        f'{enemy_rll.name} health: {enemy_rll.health}')

        def enemy_roll(player_rll, enemy_rll):
            if enemy_rll.health <= 0:
                player_rll.add_points(enemy_rll.get_value())
                print('enrll')
                return f'\nYou killed the {enemy_rll.name}'
            if player_rll.health <= 0:
                print('enrll')
                return '\nYou are dead'
            roll = random.randint(1, 20)
            if roll > player_rll.armor:
                damage = enemy_rll.attack(player)
                return (f'\n{enemy_rll.name} hit you for {damage} damage\n'
                        f'Your health: {player_rll.health}\n'
                        f'{enemy_rll.name} health: {enemy_rll.health}')
            else:
                return (f'\n{enemy_rll.name} misses!\n'
                        f'Your health: {player_rll.health}\n'
                        f'{enemy_rll.name} health: {enemy_rll.health}\n')

        def main(player_btl, enemy_btl):
            #if player_btl.health <= 0:
             #   return '\nYou are dead'
            #elif enemy_btl.health <= 0:
             #   return f'\nYou killed the {enemy_btl.name}'
            #else:
                user_input = input(f'You need to roll a dice\n'
                                   f'Roll? (y/n): ')
                if user_input == 'y':
                    return (f'{player_roll(player_btl, enemy_btl)}\n'
                            f'{enemy_roll(player_btl, enemy_btl)}')
                elif user_input == 'n':
                    return enemy_roll(player_btl, enemy_btl)

        print(main(player, enemy)) # TODO: print is not ok


def main_logic(dungeon, player):
    if player.health <= 0:
        player.del_points()
        return '\nYou are dead'
    for floor_number, floor in dungeon.floors.items():
        floor_info_logic(player, floor, floor_number)
        print(floor)
        for room in floor:
            if isinstance(room, Player):
                continue
            for i, obj in enumerate(room.get_objects()):
                if isinstance(obj, Object):
                    interact_key_object = obj.player_interact()
                    if interact_key_object:
                        inventory_logic(player, obj, room)
                        room.get_objects().insert(i, None)
                        # TODO: fix index, insert its a quick fix
                    else:
                        pass
                elif isinstance(obj, Enemy):
                    interact_key_enemy = obj.player_interact()
                    if interact_key_enemy:
                        battle_logic(player, obj)
                    else:
                        stealth_logic(player, obj)
                        battle_logic(player, obj)
                if player.health <= 0:
                    player.del_points()
                    print('main')
                    return '\nYou are dead'
                if i == len(room.get_objects()) - 1:
                    rest_logic(player)

def show_leaderboard():
    conn = sqlite3.connect('busko_game_data.db').cursor()
    conn = conn.execute(f'SELECT * FROM leaders')
    return conn.fetchall()

def end_message(dungeon, player): # TODO: key - quick fix
    bad_magician = dungeon.floors[5][-1].get_objects()[0]
    main_treasure = dungeon.floors[5][-1].get_objects()[1]
    if player.health <= 0:
        return ("It's happen sometimes, but you can try again\n"
                "Of course your score is not saved")
    if bad_magician.health <= 0 and bad_magician.key is True and main_treasure is None:
        player.save_leaderboard()
        return (f"Congratulations! You defeated the {bad_magician.name}\nand got the {get_last_treasure().name}\n"
                f"Your score: {player.points}\n"
                f"For this time, i maybe save your score in the leaderboard\n")
    if bad_magician.health <= 0 and bad_magician.key is True and main_treasure is not None:
        player.save_leaderboard()
        return (f"Congratulations! You defeat the {bad_magician.name}\nand haven't "
                f"take the {get_last_treasure().name}\n"
                f"Why haven't you taken the {get_last_treasure().name}?\n"
                f"For real, what the heck is happen with you?\n"
                f"Anyway, your score: {player.points}\n"
                f"I save your score in the leaderboard")
    if bad_magician.key is False and main_treasure is None:
        player.save_leaderboard()
        return (f"Congratulations! You little sneaky mouse, you are avoid the {bad_magician.name}\n"
                f"and got the {get_last_treasure().name}\n"
                f"Of course I don't judge you\n"
                f"What can happen if you leave such terrible and powerful magicians alive\n"
                f"Your score: {player.points}\n"
                f"I save your score in the leaderboard")
    if bad_magician.key is False and main_treasure is not None:
        return (f"You didn't defeat the magician, you didn't take the treasure.\n"
                f"I don't want to talk with you anymore.\n"
                f"3 weeks of work for nothing.\n"
                f"I don't save your score in the leaderboard")


def welcome_message(dungeon, player):
    user_input = input("\nThe voice in your head hasn't stopped buzzing\n"
                       "for weeks, it's been leading you to this dungeon.\n"
                       "But why you? What kind of voice is that?\n"
                       "An ordinary blacksmith from a small village.\n"
                       "I don't think you're going to find out.\n\n"
                       "Are you ready to continue following this voice?\n"
                       "Enter the dungeon? (y/n): ")
    if user_input == 'y':
        player.set_position(dungeon, 1)
        return f'\nYou enter the dungeon\n'
    elif user_input == 'n':
        player.hit(10000000)
        return ("You get a severe headache, you feel\n"
                "something squeezing your throat from\n"
                "the outside, the game is over.")


def get_active_enemies():
    return [Enemy(*i) for i in get_sql_data('enemies')
            if i[0] != 'Busko']


def get_sql_data(data):
    conn = sqlite3.connect('busko_game_data.db').cursor()
    conn = conn.execute(f'SELECT * FROM {data}')
    return [i[1:] for i in conn]


# noinspection PyTypeChecker
def get_active_objects():
    return [i for i in itertools.chain([Weapon(*i) for i in get_sql_data('weapons')],
                                       [Potion(*i) for i in get_sql_data('potions')],
                                       [Treasure(*i) for i in get_sql_data('treasures')
                                        if i[0] != 'diamond of exhaustion'])]


def get_first_weapon():
    return [Weapon(*i) for i in get_sql_data('weapons') if i[0] == 'stick'][0]


def get_first_potion():
    return [Potion(*i) for i in get_sql_data('potions') if i[0] == 'healing potion'][0]


def get_last_treasure():
    return [Treasure(*i) for i in get_sql_data('treasures') if i[0] == 'diamond of exhaustion'][0]


def get_last_enemy():
    return [Enemy(*i) for i in get_sql_data('enemies') if i[0] == 'Busko'][0]


def fill_dungeon(dungeon):
    for floor_number, floor in dungeon.floors.items():
        if floor_number == 1:
            room = Room()
            room.add_object(get_first_weapon())
            room.add_object(get_first_potion())
            floor.append(room)
        elif floor_number == 5:
            room = Room()
            room.add_object(get_last_enemy())
            room.add_object(get_last_treasure())
            floor.append(room)
        else:
            for _ in range(random.randint(1, 3)):
                room = Room()
                for _ in range(random.randint(1, 3)):
                    room.add_object(random.choice(get_active_objects()))
                room.add_object(random.choice(get_active_enemies()))
                floor.append(room)
