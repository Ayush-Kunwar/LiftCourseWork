class Person:
    def __init__(self, start_floor: int, end_floor: int):
        self.start_floor = start_floor
        self.end_floor = end_floor
        self.direction = self.set_direction()

    def set_direction(self):
        # sets direction (up or down) in the lift depending of start and end floor
        if self.start > self.end:
            return "down"
        else:
            return "up"
    
    def get_end_floor(self):
        # returns floor where person gets off
        return self.end_floor

class Lift:
    def __init__(self, top_floor: int, capacity: int):
        self.current_floor = 1
        self.direction = "up"
        self.people = []
        self.capacity = capacity
        self.top_floor = top_floor
    
    def get_capacity(self):

        return self.capacity

    def add_person(self, *people: Person):
        for person in people:
            if isinstance(person, int):
                self.people.append(person)
            else:
                raise ValueError("Floor request must be an integer")
            
    def change_direction(self):
        if self.direction == "up":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "up"

    def set_floor(self, floor: int):
        self.current_floor = floor

    def __repr__(self):
        return f"Lift(floor={self.floor}, direction='{self.direction}', requests={self.requests})"