from fileHandling import fileHandling
class Person:
    def __init__(self, startFloor: int, endFloor: int):
        self.startFloor = startFloor
        self.endFloor = endFloor
        self.direction = self.set_direction()

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


def loadRequests(filename = "data.txt"): #convert the list of requests into individual objects
    requests = fileHandling(filename)[0]
    requestsAsClass = []
    for i in range(len(requests)): #for each floor
        floor = []
        for j in range(len(requests[i])): #for each person
            person = Person(i+1, requests[i][j]) #make them a Person with current floor and destination as attributes
            floor.append(person) #add to list
        requestsAsClass.append(floor)
    return requestsAsClass

filename = "input2.txt"
requests = loadRequests(filename)

class Lift:
    def __init__(self, liftNumber: int, topFloor: int, capacity: int, bottomFloor: int = 1):
        self.liftNumber = liftNumber
        self.currentFloor = bottomFloor
        self.direction = "up"
        self.peopleLift = []
        self.capacity = capacity
        self.numberOfPeople = 0
        self.bottomFloor = bottomFloor
        self.topFloor = topFloor

    def get_liftNumber(self) -> int:
        """Returns lift number"""
        return self.liftNumber
    
    def get_direction(self) -> str:
        """Returns direction the lift is traveling in"""
        return self.direction
    
    def get_number_of_people(self) -> int:
        """Returns Current Capacity of the lift"""
        return self.numberOfPeople
    
    def check_if_full(self) -> bool:
        """Checks if lift is full"""
        if self.numberOfPeople == self.capacity:
            return True
        else:
            return False

    def add_person(self):
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

    def remove_people(self):
        """Remove people if they are at thier destination floor"""
        addingRequest = []
        for person in self.peopleLift:
            if person.get_end_floor() == self.currentFloor:
                addingRequest.append(person)
                self.numberOfPeople -= 1
            elif self.checkEnd():
                addingRequest.append(person)
                requests[self.currentFloor - 1].append(person)
                self.numberOfPeople -= 1
        
        for person in addingRequest:
            self.peopleLift.remove(person)

    def get_current_floor(self) -> int:
        """Returns current floor of the lift"""
        return self.currentFloor
    
    def change_direction(self):
        """Changes direction of the lift"""
        if self.direction == "up":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "up"
    
    def checkAhead(self) -> bool: 
        """Check if there are valid requests ahead in the current direction"""
        if self.direction == "up":
            for x in range(self.currentFloor + 1, self.topFloor):
                if requests[x - 1]:
                    return True
            return False
        elif self.direction == "down":
            for x in range(self.currentFloor - 1, self.bottomFloor, -1):
                if requests[x - 1]:
                    return True
            return False
    
    def checkNoRequests(self) -> bool:
        """Checks if there no people/requests for the lift to respond to"""
        if self.numberOfPeople != 0:
            return False
        
        for x in range(self.currentFloor + 1, self.topFloor): #Checks if they are any requests above the lift
            if requests[x - 1]:
                return False
        for x in range(self.currentFloor - 1, self.bottomFloor, -1): #Checks if they are any requests below the lift
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
    
    def move_lift(self):
        """Moves lift by one floor"""
        if (self.numberOfPeople == 0 and not self.checkAhead()) or self.checkEnd():
            self.change_direction()
        else:
            if self.direction == "up":
                self.currentFloor += 1
            elif self.direction == "down":
                self.currentFloor -= 1

    def int_peopleLift(self):
        """Represents the people in the lift as their destination floor in an array"""
        numPeople = []
        for person in self.peopleLift:
            numPeople.append(person.get_end_floor())
        return numPeople

    def __repr__(self) -> str:
        """Returns a string representation of the Lift object"""
        return (f"\nLift {self.liftNumber} Information"
                f"\nDirection: {self.direction} || Current Floor: {self.currentFloor}"
                f"\nPeople in Lift: {self.int_peopleLift()} || {self.numberOfPeople}/{self.capacity}" 
                f"\nOperating Floors: {self.bottomFloor}-{self.topFloor}")
     
def print_requests():
    print("\nAll Requests")
    for x in range(len(requests)):
        print(f"Floor: {x + 1}")
        print(requests[x])

def lift_setup(numberOfLifts: int = 1):
    lifts = []
    capacity = fileHandling(filename)[1]
    floors = fileHandling(filename)[2]
    invalid = False
    topfloor = None
    bottomFloor = None

    for x in range(1, numberOfLifts + 1):
        topfloor = None
        bottomFloor = None

        while invalid or topfloor == None or bottomFloor >= topfloor:
            invalid = False
            topfloor = None
            bottomFloor = None

            bottomFloor= int(input(f"\nWhat is the bottom floor of Lift {x} (min: 1): "))
            topfloor = int(input(f"What is the top floor of Lift {x} (max: {floors}): "))

            if bottomFloor >= topfloor or topfloor > floors or bottomFloor < 1:
                print("\nInputs are Invalid.\n")
                invalid = True
    
        lift = Lift(liftNumber = x, topFloor = topfloor, capacity = capacity, bottomFloor = bottomFloor)
        lifts.append(lift)

    return lifts


def look():
    numofrequests = 1
    floors = fileHandling(filename)[2]
    numberOfLifts = 0

    while numberOfLifts < 1:
        numberOfLifts = int(input(f"How many lifts would you like in your {floors} story building?\n"))
    lifts = lift_setup(numberOfLifts = numberOfLifts)

    print_requests()
    while numofrequests != 0:
        for lift in lifts:
            if not lift.checkNoRequests():
                switch = False
                if not lift.checkEnd():
                    """Adds people to the lift"""
                    lift.add_person()
                    print(f"\nAdding People to Lift {lift.get_liftNumber()} ...\n")
                    print_requests()
                    print(lift)
                    pause = input("\nPress Enter to continue.\n")

                if ((lift.get_number_of_people() == 0 and not lift.checkAhead()) or lift.checkEnd()):
                    switch = True

                """Moves the lift/Change direction of the lift"""
                lift.move_lift()
                if not switch:
                    print(f"\nMoving Lift {lift.get_liftNumber()} ...\n")
                elif switch:
                    print(f"\nLift {lift.get_liftNumber()} now going {lift.get_direction()} ...\n")
                print(lift)

                """Removes people from the lift"""
                lift.remove_people()
                print(f"\nRemoving People from Lift {lift.get_liftNumber()} ...\n")
                print_requests()
                print(lift)
                pause = input("\nPress Enter to continue.\n")
                
            else:
                pause = ""
                print(f"\nLift {lift.get_liftNumber()} has no requests.\n")
                pause = input("\nType 'b' to See All Requests.\nPress Enter to continue.\n")
                if pause.lower() == "b":
                    print_requests()
                    
            print("----------------------------------------")
            
            numofrequests = 0
            for lift in lifts:
                numofrequests += lift.get_number_of_people()
            for x in requests:
                numofrequests += len(x)
                
    print("\nSimulation Finished\n")
    
if __name__ == "__main__":
    look()
