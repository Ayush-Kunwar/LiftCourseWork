class Person:
    def __init__(self, startFloor: int, endFloor: int):
        self.startFloor = startFloor
        self.endFloor = endFloor
        self.direction = self.set_direction()
        self.wait_time = 0

    def set_direction(self) -> str:
        """Sets direction (up or down) in the lift depending of start and end floor"""
        if self.startFloor > self.endFloor:
            return "down"
        else:
            return "up"
    
    def get_direction(self) -> str:
        """Returns the direction the person is travelling in"""
        return self.direction
    
    def get_end_floor(self) -> int:
        """Returns destination floor of the person"""
        return self.endFloor
    
    def __repr__(self) -> str:
        """Returns a string representation of the Person object"""
        return f"{self.endFloor} || {self.direction}"