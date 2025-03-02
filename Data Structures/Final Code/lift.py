from statistics_1 import Statistics

class Lift:
    def __init__(self, liftNumber: int, topFloor: int, capacity: int, bottomFloor: int = 1, currentState = "add"):
        self.liftNumber = liftNumber
        self.currentFloor = bottomFloor
        self.direction = "up"
        self.peopleLift = []
        self.capacity = capacity
        self.numberOfPeople = 0
        self.bottomFloor = bottomFloor
        self.topFloor = topFloor
        self.state = currentState
        self.statistics = Statistics()  # Link statistics to the lift

    def get_liftNumber(self) -> int:
        """Returns lift number"""
        return self.liftNumber
    
    def get_direction(self) -> str:
        """Returns direction the lift is traveling in"""
        return self.direction
    def set_direction(self, direction: int):
        self.direction = direction
    
    def get_number_of_people(self) -> int:
        """Returns current capacity of the lift"""
        return self.numberOfPeople
    
    def get_state(self):
        """Returns current state of the lift"""
        return self.state
    
    def set_state(self, state: str):
        """Set current state of lift """
        self.state = state 
    
    def set_floor(self, floor: int):
        self.currentFloor = floor

    def check_if_full(self) -> bool:
        """Checks if lift is full"""
        if self.numberOfPeople == self.capacity:
            return True
        else:
            return False

    def add_person(self, requests):
        """Adds people to the lift"""
        removingPeople = []
    
        for person in requests[self.currentFloor - 1]:
            #if lift is not full and the person is traving in the same direction as the lift
            if not self.check_if_full() and person.get_direction() == self.direction: 
                #if the lift goes to person's destination floor
                if (self.direction == "up" and person.get_end_floor() <= self.topFloor) or (self.direction == "down" and person.get_end_floor() >= self.bottomFloor):
                    self.peopleLift.append(person)
                    removingPeople.append(person)
                    self.numberOfPeople += 1

                    self.statistics.record_wait_time(person.wait_time)
                    print(f"Recorded wait time for person at floor {person.startFloor} with wait time {person.get_wait_time()}")  # Debug statement
        for person in removingPeople:
            requests[self.currentFloor - 1].remove(person)
        
        #for loop above prorities people who would only take one lift to get to there destination
        removingPeople = []

        for person in requests[self.currentFloor - 1]:
            if not self.check_if_full() and person.get_direction() == self.direction: 
                self.peopleLift.append(person)
                removingPeople.append(person)
                self.numberOfPeople += 1

        for person in removingPeople:
            requests[self.currentFloor - 1].remove(person)
        return requests

    def remove_people(self, requests):
        """Remove people if they are at thier destination floor"""
        addingRequest = []
        for person in self.peopleLift:
            if person.get_end_floor() == self.currentFloor:
                addingRequest.append(person)
                self.numberOfPeople -= 1
                self.statistics.record_travel_time(person.travel_time)
            elif self.checkEnd():
                addingRequest.append(person)
                requests[self.currentFloor - 1].append(person)
                self.numberOfPeople -= 1
        
        for person in addingRequest:
            self.peopleLift.remove(person)
        return requests
    
    def get_current_floor(self) -> int:
        """Returns current floor of the lift"""
        return self.currentFloor
    
    def change_direction(self):
        """Changes direction of the lift"""
        if self.direction == "up" and self.currentFloor != self.bottomFloor:
            self.direction = "down"
        elif self.direction == "down" and self.currentFloor != self.topFloor:
            self.direction = "up"
    
    def checkAhead(self, requests) -> bool: 
        """Check if there are valid requests ahead in the current direction"""
        if self.direction == "up":
            for x in range(self.currentFloor + 1, self.topFloor + 1):
                if requests[x - 1]:
                    return True
            return False
        elif self.direction == "down":
            for x in range(self.currentFloor - 1, self.bottomFloor - 1, -1):
                if requests[x - 1]:
                    return True
            return False
    
    def checkNoRequests(self, requests) -> bool:
        """Checks if there no people/requests for the lift to respond to"""
        if self.numberOfPeople != 0:
            return False
        
        for x in range(self.currentFloor + 1, self.topFloor + 1): #Checks if they are any requests above the lift
            if requests[x - 1]:
                return False
        for x in range(self.currentFloor - 1, self.bottomFloor - 1, -1): #Checks if they are any requests below the lift
            if requests[x - 1]:
                return False
            
        if self.checkEnd(): #Checks if lift is at the bottom or top
            if self.checkTop(): 
                for person in requests[self.currentFloor - 1]: #Checks if there are any requests to go down from Top
                    if person.get_direction() == "down":
                        return False
                    
            elif self.checkBottom():
                for person in requests[self.currentFloor - 1]: #Checks if there are any requests to go up from Bottom
                    if person.get_direction() == "up":
                        return False
                    
        else:
            if requests[self.currentFloor - 1]: #Checks if there are any people on curretn floor (not top or bottom)
                return False
        return True

    def checkTop(self) -> bool:
        """Checks if lift is at the top floor"""
        if self.direction == "up":
            return self.currentFloor == self.topFloor
        
    def checkBottom(self) -> bool:
        """Checks if lift is at the bottom floor"""
        if self.direction == "down":
            return self.currentFloor == self.bottomFloor
        
    def checkEnd(self) -> bool:
        """Checks if lift is at the top or bottom floor"""
        return self.checkTop() or self.checkBottom()
    
    def move_lift(self, requests):
        """Moves lift by one floor"""
        if (self.numberOfPeople == 0 and not self.checkAhead(requests)) or self.checkEnd():
            self.change_direction()
        else:
            if self.direction == "up":
                self.currentFloor += 1
            elif self.direction == "down":
                self.currentFloor -= 1
            self.statistics.record_lift_movement()  # Track movement
            self.statistics.record_lift_utilization(self.numberOfPeople, self.capacity)

    def move_lift_scan(self):
        """Moves lift by one floor"""
        if self.checkEnd():
            self.change_direction()
        else:
            if self.direction == "up":
                self.currentFloor += 1
            elif self.direction == "down":
                self.currentFloor -= 1
            self.statistics.record_lift_movement()  # Track movement
            self.statistics.record_lift_utilization(self.numberOfPeople, self.capacity)

    def int_peopleLift(self):
        """Represents the people in the lift as their destination floor in an array"""
        numPeople = []
        for person in self.peopleLift:
            numPeople.append(person.get_end_floor())
        return numPeople
    
    def update_waiting_times(self, requests):
        """Increment wait times only for passengers who have arrived but not entered the lift."""
        for floor_requests in requests:
            for person in floor_requests:
                if person not in self.peopleLift:  # Only increment if not yet in the lift
                    person.increment_wait_time()
        


    def update_travel_times(self):
        """Increment travel times for people inside the lift."""
        for person in self.peopleLift:
            person.increment_travel_time()
    def __repr__(self) -> str:
        """Returns a string representation of the Lift object"""
        return (f"\n\033[1m\033[4mLift {self.liftNumber} Information\033[0m"
                f"\n\033[2mDirection: {self.direction} || Current Floor: {self.currentFloor}"
                f"\nPeople in Lift: {self.int_peopleLift()} || {self.numberOfPeople}/{self.capacity}" 
                f"\nOperating Floors: {self.bottomFloor}-{self.topFloor}\033[0m")
