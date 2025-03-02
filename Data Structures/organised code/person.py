class Person:
    def __init__(self, startFloor: int, endFloor: int):
        self.startFloor = startFloor
        self.endFloor = endFloor
        self.direction = self.set_direction()
        self.wait_time = 0  # Track how long they wait
        self.travel_time = 0  # Track how long they are in the lift
        
    def set_direction(self) -> str:
        """Sets direction (up or down) in the lift depending of start and end floor"""
        if self.startFloor > self.endFloor:
            return "down"
        else:
            return "up"
    
    def get_direction(self) -> str:
        """Returns the direction the person is travelling in"""
        return self.direction
    
    def get_wait_time(self) -> int:
        """Returns time waited by person"""
        return self.wait_time

    def get_end_floor(self) -> int:
        """Returns destination floor of the person"""
        return self.endFloor
    
    def increment_wait_time(self):
        """Increment the wait time while waiting for a lift."""
        self.wait_time += 1

    def increment_travel_time(self):
        """Increment the travel time while in the lift."""
        self.travel_time += 1

    def __repr__(self) -> str:
        """Returns a string representation of the Person object"""
        return f"{self.endFloor} || {self.direction}"