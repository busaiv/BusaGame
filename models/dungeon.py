class Dungeon:
    def __init__(self, name):
        self.name = name
        self.floors = {}

    def __repr__(self):
        return f'{self.name}({self.floors})'

    def set_floors(self, floors):
        #if floors is not dict:
         #   raise TypeError('floors must be a dict')
        self.floors = floors

    def add_rooms(self, floor, room):
        if floor not in self.floors.keys():
            raise ValueError('floor does not exist')
        #if room is not int:
         #   raise TypeError('room must be an int')
        self.floors[floor].append(room)

    def get_floors(self):
        return self.floors

class Room:
    def __init__(self):
        self.name = 'room'
        self.objects = []

    def __repr__(self):
        return f'{self.name}{self.objects}'

    #def set_description(self, description):
        #if description is not str:
         #   raise TypeError('description must be a str')
     #   self.description = description

   # def get_description(self):
    #    return self.description

    def add_object(self, room_object):
        self.objects.append(room_object)
        return self


    def get_objects(self):
        return self.objects

    def remove_object(self, room_object):
        return self.objects.pop(self.objects.index(room_object))

    def get_current_object(self):
        return self.objects






