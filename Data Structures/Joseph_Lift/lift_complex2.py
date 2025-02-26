from fileHandling import fileHandling
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

filename = "input2.txt" ##change filename to change data
requests = loadRequests(filename)

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

    def get_liftNumber(self) -> int:
        """Returns lift number"""
        return self.liftNumber
    
    def get_direction(self) -> str:
        """Returns direction the lift is traveling in"""
        return self.direction
    
    def get_number_of_people(self) -> int:
        """Returns current capacity of the lift"""
        return self.numberOfPeople
    
    def get_state(self):
        """Returns current state of the lift"""
        return self.state
    
    def set_state(self, state: str):
        self.state = state
        
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
        if self.direction == "up" and self.currentFloor != self.bottomFloor:
            self.direction = "down"
        elif self.direction == "down" and self.currentFloor != self.topFloor:
            self.direction = "up"
    
    def checkAhead(self) -> bool: 
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
    
    def checkNoRequests(self) -> bool:
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
        return (f"\n\033[1m\033[4mLift {self.liftNumber} Information\033[0m"
                f"\n\033[2mDirection: {self.direction} || Current Floor: {self.currentFloor}"
                f"\nPeople in Lift: {self.int_peopleLift()} || {self.numberOfPeople}/{self.capacity}" 
                f"\nOperating Floors: {self.bottomFloor}-{self.topFloor}\033[0m")
     
def print_requests():
    print("\n\033[1m\033[4mAll Requests\033[0m")
    for x in range(len(requests)):
        print(f"Floor: {x + 1}")
        print("\033[2m" ,requests[x], "\033[0m")

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
    global requests, filename
    requests = loadRequests(filename)
    numofrequests = 1
    floors = fileHandling(filename)[2]
    numberOfLifts = 0
    exit = False
    passes = 0
    #states = ["add", "move", "remove", "idle"]

    while numberOfLifts < 1:
        numberOfLifts = int(input(f"\nHow many lifts would you like in your {floors} story building?\033[0m\n"))
    lifts = lift_setup(numberOfLifts = numberOfLifts)

    print_requests()
    while numofrequests != 0 and not exit:
        exit = False
        noRemove = False
        for lift in lifts:
            """Removes people from the lift"""
            if lift.get_state() == "remove": #remove only if there are people to remove 
                noRemove = False
                peopleBefore = lift.get_number_of_people()
                lift.remove_people()
                if not peopleBefore == lift.get_number_of_people():
                    print(f"\n\033[1mRemoving People from Lift {lift.get_liftNumber()} ...\033[0m\n")
                    if lift.checkEnd():
                        print_requests()
                    print(lift)
                    if ((lift.get_number_of_people() == 0 and not lift.checkAhead()) or lift.checkEnd()): #change direction
                        lift.set_state("move")
                    else: 
                        lift.set_state("add")
                elif ((lift.get_number_of_people() == 0 and not lift.checkAhead()) or lift.checkEnd()): #change direction
                    lift.set_state("move")
                else:
                    noRemove = True
                    lift.set_state("add")
                
            """Check if has no requests to respond to"""
            if lift.checkNoRequests():
                lift.set_state("idle")

                """Moves the lift/Change direction of the lift"""
            if lift.get_state() == "move":
                if ((lift.get_number_of_people() == 0 and not lift.checkAhead()) or lift.checkEnd()): #check to see if the lift is changing direction instead of moving
                    lift.move_lift()
                    print(f"\n\033[1mLift {lift.get_liftNumber()} now going {lift.get_direction()} ...\033[0m\n")
                    print(lift)
                    lift.set_state("add")
                else: 
                    lift.move_lift()
                    print(f"\n\033[1mMoving Lift {lift.get_liftNumber()} ...\033[0m\n")
                    print(lift)
                    lift.set_state("remove")
                
                """Adds people to the lift"""
            if lift.get_state() == "add": #add only if there are people to add
                peopleBefore = lift.get_number_of_people()
                lift.add_person()
                if not peopleBefore == lift.get_number_of_people():        
                    print(f"\n\033[1mAdding People to Lift {lift.get_liftNumber()} ...\033[0m\n")
                    print_requests()
                    print(lift)
                    lift.set_state("move")
                elif noRemove or passes == 0: #moving lift if the lift doesn't add or remove people
                    lift.move_lift()
                    print(f"\n\033[1mMoving Lift {lift.get_liftNumber()} ...\033[0m\n")
                    print(lift)
                    lift.set_state("remove")
                else:
                    lift.set_state("move")

            """When if has no requests to respond to"""
            if lift.get_state() == "idle":
                print(f"\n\033[1mLift {lift.get_liftNumber()} has no more requests.\033[0m\n")
                pause = input("\n\033[1mType 'a' to See All Requests.\nType 'l' to See All Lift Information.\nType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                if pause.lower() == "a":
                    print_requests()
                    pause = input("\n\033[1mType 'l' to See All Lift Information.\nType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                    if pause.lower() == "l":
                        for lift in lifts:
                            print(lift)
                        pause = input("\n\033[1mType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                elif pause.lower() == "l":
                    for lift in lifts:
                        print(lift)
                    pause = input("\n\033[1mType 'a' to See All Requests.\nType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                    if pause.lower() == "a":
                        print_requests()
                        pause = input("\n\033[1mType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                if pause.lower() == "e":
                    exit = True
                lift.set_state("remove")
            
            """Pause for the simulation"""
            if not lift.checkNoRequests():
                pause = input("\n\033[1mType 'l' to See All Lift Information.\nType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                if pause.lower() == "l":
                    for lift in lifts:
                        print(lift)
                    pause = input("\n\033[1mPress Enter to continue.\033[0m\n")
                elif pause.lower() == "e":
                    exit = True


        print("\n\033[1m----------------------------------------\033[0m\n") #1 time has passed
        passes += 1

        numofrequests = 0
        for lift in lifts:
            numofrequests += lift.get_number_of_people()
        for x in requests:
            numofrequests += len(x)

    print("Passes: ", passes)
    pause = input("\n\033[1mSimulation Finished\nType 'r' to Restart.\nPress Enter to Exit.\033[0m\n")
    if pause.lower() == "r":
        look()
    
if __name__ == "__main__":
    look()