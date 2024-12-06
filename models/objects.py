import sqlite3

class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'{self.name}'

    def player_interact(self):
        pass

class Potion(Object):
    def __init__(self, name, description, effect, uses):
        super().__init__(name, description)
        self.effect = effect
        self.uses = uses

    #def __repr__(self):
     #   return f'{self.name}({self.description}, {self.effect}, {self.uses})'

    def save_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        if self.name in [i[0] for i in conn.execute('SELECT name FROM potions').fetchall()]:
            conn.execute('UPDATE potions SET description = ?, effect = ?, uses = ? WHERE name = ?',
                         (self.description, self.effect, self.uses, self.name))
            conn.connection.commit()
        else:
            conn.execute('INSERT INTO potions (name, description, effect, uses) VALUES (?, ?, ?, ?)',
                         (self.name, self.description, self.effect, self.uses))
            conn.connection.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        self.description = conn.execute('SELECT description FROM potions WHERE name = ?',
                                        (self.name,)).fetchone()[0]
        self.effect = conn.execute('SELECT effect FROM potions WHERE name = ?',
                                   (self.name,)).fetchone()[0]
        self.uses = conn.execute('SELECT uses FROM potions WHERE name = ?',
                                 (self.name,)).fetchone()[0]
        conn.close()

    def use(self, player):
        if self.uses <= 0:
            raise ValueError('No more uses left')
        self.uses -= 1
        player.health += self.effect


    def player_interact(self):
        key = input(f'\nYou found a {self.name}.\n'
                    f'{self.description}\n'
                    f'Effect: {self.effect}\n'
                    f'Uses: {self.uses}\n'
                    f'Do you want to take it? (y/n): ')
        if key == 'y':
            return True
        elif key == 'n':
            return False

class Weapon(Object):
    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self.damage = damage

    #def __repr__(self):
     #   return f'{self.name}({self.description}, {self.damage})'

    def save_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        if self.name in [i[0] for i in conn.execute('SELECT name FROM weapons').fetchall()]:
            conn.execute('UPDATE weapons SET description = ?, damage = ? WHERE name = ?',
                         (self.description, self.damage, self.name))
            conn.connection.commit()
        else:
            conn.execute('INSERT INTO weapons (name, description, damage) VALUES (?, ?, ?)',
                         (self.name, self.description, self.damage))
            conn.connection.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        self.description = conn.execute('SELECT description FROM weapons WHERE name = ?', (self.name,)).fetchone()[0]
        self.damage = conn.execute('SELECT damage FROM weapons WHERE name = ?', (self.name,)).fetchone()[0]
        conn.close()

    def player_interact(self):
        key = input(f'\nYou found a {self.name}.\n'
                    f'{self.description}\n'
                    f'Damage: {self.damage}\n'
                    f'Do you want to equip it? (y/n): ')
        if key == 'y':
            return True
        elif key == 'n':
            return False

    def set_damage(self, damage):
        self.damage = damage

    def attack(self):
        return self.damage  # будет вычитываться из хп

class Treasure(Object):
    def __init__(self, name, description, value):
        super().__init__(name, description)
        self.value = value

    #def __repr__(self):
     #   return f'{self.name}({self.description}, {self.value})'

    def save_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        if self.name in [i[0] for i in conn.execute('SELECT name FROM treasures').fetchall()]:
            conn.execute('UPDATE treasures SET description = ?, value = ? WHERE name = ?',
                         (self.description, self.value, self.name))
            conn.connection.commit()
        else:
            conn.execute('INSERT INTO treasures (name, description, value) VALUES (?, ?, ?)',
                         (self.name, self.description, self.value))
            conn.connection.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect('busko_game_data.db').cursor()
        self.description = conn.execute('SELECT description FROM treasures WHERE name = ?',
                                        (self.name,)).fetchone()[0]
        self.value = conn.execute('SELECT value FROM treasures WHERE name = ?',
                                  (self.name,)).fetchone()[0]
        conn.close()

    def player_interact(self):
        key = input(f'\nYou found a {self.name}.\n'
                    f'{self.description}\n'
                    f'Value: {self.value}\n'
                    f'Do you want to take it? (y/n): ')
        if key == 'y':
            return True
        elif key == 'n':
            return False

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value