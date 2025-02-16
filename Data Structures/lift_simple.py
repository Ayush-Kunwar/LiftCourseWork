class Person:
    def __init__(self, start_floor: int, end_floor: int):
        self.start_floor = start_floor
        self.end_floor = end_floor
        self.direction = self.set_direction()

    def set_direction(self) -> str:
        # sets direction (up or down) in the lift depending of start and end floor
        if self.start > self.end:
            return "down"
        else:
            return "up"
    
    def get_end_floor(self) -> int:
        # returns floor where person gets off
        return self.end_floor

class Lift:
    def __init__(self, top_floor: int, capacity: int, bottom_floor: int = 1):
        self.current_floor = bottom_floor
        self.direction = "up"
        self.people = []
        self.capacity = capacity
        self.current_capacity = capacity
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
    
    def get_current_capacity(self) -> int:
        return self.current_capacity
    
    def check_if_full(self) -> bool:
        if self.current_capacity == self.capacity:
            return True
        else:
            return False

    def add_person(self, *people_add: Person):
        for person in people_add:
            self.people.append(person)
            self.current_capacity -= 1
    
    def remove_person(self, *people_remove: Person):
        for x in self.people:
            for person in people_remove:
                if x == person:
                    self.people.remove(person)
                    self.current_capacity += 1

    def get_current_floor(self) -> int:
        return self.current_floor
    
    def change_direction(self):
        if self.direction == "up":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "up"

    def move_lift(self):
        if self.direction == "up":
            self.current_floor += 1
        elif self.direction == "down":
            self.current_floor -= 1

    def __repr__(self):
        return (f"Lift(current_floor={self.current_floor}, direction={self.direction}, "
                f"people=[{self.people}], capacity={self.capacity}, "
                f"current_capacity={self.current_capacity}, top_floor={self.top_floor})")
