class Person:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def direction(self):
        if self.start > self.end:
            return "down"
        return "up"

class Lift:
    def __init__(self, floor, direction):
        self.floor = floor
        self.direction = direction