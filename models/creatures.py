import sqlite3
from models.objects import Weapon
import random

class Player:
    def __init__(self, name, health, damage, armor, stealth_bonus, points):
        self.position = None
        self.name = name
        self.health = health
        self.damage = damage
        self.stealth_bonus = stealth_bonus
        self.weapon = Weapon('fists', 'its just your hands, remember that', 2)
        self.armor = armor
        self.inventory = {'potion': [], 'treasure': []}
        self.points = points

    def __repr__(self):
        return f'{self.name}({self.health}, {self.damage})'

    def save_leaderboard(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        data = conn.execute('SELECT * FROM leaders WHERE name = ?', (self.name,)).fetchone()
        if data:
            if self.points > data[2]:
                conn.execute('UPDATE leaders SET score = ? WHERE name = ?',
                             (self.points, self.name))
        else:
            conn.execute('INSERT INTO leaders (name, score) VALUES (?, ?)',
                     (self.name, self.points))
        conn.connection.commit()
        conn.close()

    def save_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        if self.name in [i[0] for i in conn.execute('SELECT name FROM players').fetchall()]:
            conn.execute('UPDATE players SET health = ?, damage = ?, armor = ?, stealth_bonus = ?, points = ?'
                         'WHERE name = ?',
                         (self.health, self.damage, self.armor, self.stealth_bonus, self.points, self.name))
            conn.connection.commit()
        else:
            conn.execute('INSERT INTO players (name, health, damage, armor, stealth_bonus, points) '
                         'VALUES (?, ?, ?, ?, ?, ?)',
                         (self.name, self.health, self.damage, self.armor, self.stealth_bonus, self.points))
            conn.connection.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        self.health = conn.execute('SELECT health FROM players WHERE name = ?',
                                   (self.name,)).fetchone()[0]
        self.damage = conn.execute('SELECT damage FROM players WHERE name = ?',
                                   (self.name,)).fetchone()[0]
        self.armor = conn.execute('SELECT armor FROM players WHERE name = ?',
                                  (self.name,)).fetchone()[0]
        self.stealth_bonus = conn.execute('SELECT stealth_bonus FROM players WHERE name = ?',
                                          (self.name,)).fetchone()[0]
        self.points = conn.execute('SELECT points FROM players WHERE name = ?',
                                   (self.name,)).fetchone()[0]
        conn.close()

    def set_name(self, name):
        self.name = name

    def set_health(self, health):
        self.health = health

    def set_damage(self, damage):
        self.damage = damage

    def hit(self, damage):
        self.health -= damage

    def healing(self, healing):
        self.health += healing

    def take_treasure(self, element):
        self.inventory['treasure'].append(element)

    def take_potion(self, element):
        self.inventory['potion'].append(element)

    def del_treasure(self, element):
        self.inventory['treasure'].remove(element)

    def del_potion(self, element):
        self.inventory['potion'].remove(element)

    def attack(self, enemy):
        if self.damage == 1:
            enemy.hit(self.damage)
            return self.damage
        enemy.hit(damage := random.randint(1, int(self.damage)))
        return damage

    def stealth_attack(self, enemy):
        enemy.hit(damage := self.damage + self.stealth_bonus)
        return damage

    def set_weapon(self, weapon):
        self.weapon = weapon

    def equip_weapon(self, weapon):
        self.weapon = weapon
        self.damage = weapon.damage

    def set_position(self, dungeon, floor):
        dungeon.floors[floor].insert(0, self)
        self.position = floor

    def get_position_data(self):
        return self.position

    def get_points(self):
        return self.points

    def add_points(self, obj):
        self.points += obj

    def del_points(self):
        self.points = 0

    def get_position(self):
        return f'You are in the {self.position} floor.'



class Enemy:
    def __init__(self, name, story, health, damage, armor, alertness, value):
        self.name = name
        self.story = story
        self.health = health
        self.damage = damage
        self.armor = armor
        self.alertness = alertness
        self.value = value
        self.key = True

    def __repr__(self):
        return f'{self.name}'

    def save_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        if self.name in [i[0] for i in conn.execute('SELECT name FROM enemies').fetchall()]:
            conn.execute('UPDATE enemies SET story = ?, health = ?, damage = ?, armor = ?,'
                         'alertness = ?, value = ? '
                         'WHERE name = ?',
                         (self.story, self.health, self.damage, self.armor, self.alertness,
                          self.value, self.name))
            conn.connection.commit()
        else:
            conn.execute('INSERT INTO enemies (name, story, health, damage, armor, alertness, value) '
                         'VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (self.name, self.story, self.health, self.damage, self.armor,
                          self.alertness, self.value))
            conn.connection.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        self.story = conn.execute('SELECT story FROM enemies WHERE name = ?',
                                  (self.name,)).fetchone()[0]
        self.health = conn.execute('SELECT health FROM enemies WHERE name = ?',
                                   (self.name,)).fetchone()[0]
        self.damage = conn.execute('SELECT damage FROM enemies WHERE name = ?',
                                   (self.name,)).fetchone()[0]
        self.armor = conn.execute('SELECT armor FROM enemies WHERE name = ?',
                                  (self.name,)).fetchone()[0]
        self.alertness = conn.execute('SELECT alertness FROM enemies WHERE name = ?',
                                      (self.name,)).fetchone()[0]
        self.value = conn.execute('SELECT value FROM enemies WHERE name = ?',
                                  (self.name,)).fetchone()[0]
        conn.close()

    def set_name(self, name):
        self.name = name

    def set_story(self, story):
        self.story = story

    def set_health(self, health):
        self.health = health

    def set_damage(self, damage):
        self.damage = damage

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def hit(self, damage):
        self.health -= damage

    def healing(self, healing):
        self.health += healing

    def attack(self, enemy):
        if self.damage == 1:
            enemy.hit(self.damage)
            return self.damage
        enemy.hit(damage := random.randint(1, int(self.damage)))
        return damage

    def player_interact(self):
        user_input = input(f'\nYou see a {self.name}\n{self.story}\nWhat you gonna do?.\n(attack/hide): ')
        if user_input == 'attack':
            return True
        elif user_input == 'hide':
            return False