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
        return self.direction
    
    def get_end_floor(self) -> int:
        """Returns destination floor of the person"""
        return self.endFloor
    
    def __repr__(self) -> str:
        """Returns a string representation of the Person object"""
        #return f"Person(startFloor={self.startFloor}, endFloor={self.endFloor}, direction={self.direction})"
        return f"{self.endFloor}"


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

filename = "input3.txt"
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

    def remove_people(self):
        """Remove people if they are at thier destination floor"""
        for person in self.peopleLift:
            if person.get_end_floor() == self.currentFloor:
                self.peopleLift.remove(person)
                self.numberOfPeople -= 1

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
        """Check if there are valid requests ahead in the current direction."""
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
    
    def checkEnd(self) -> bool:
        """Checks if lift is at the top or bottom floor"""
        if self.direction == "up":
            return self.currentFloor == self.topFloor
        elif self.direction == "down":
            return self.currentFloor == self.bottomFloor
    
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
        """Reprents the people in the lift as their destination floor"""
        numPeople = []
        for person in self.peopleLift:
            numPeople.append(person.get_end_floor())
        return numPeople

    def __repr__(self) -> str:
        """Returns a string representation of the Lift object"""
        #return (f"Lift(currentFloor={self.currentFloor}, direction={self.direction}, "
        #        f"capacity={self.capacity}, numberOfPeople={self.numberOfPeople}, "
        #        f"bottomFloor={self.bottomFloor}, topFloor={self.topFloor})")  
        return (f"\nLift {self.liftNumber} Information"
                f"\nDirection: {self.direction} || Current Floor: {self.currentFloor}"
                f"\nPeople in Lift: {self.int_peopleLift()} || {self.numberOfPeople}/{self.capacity}" 
                f"\nOperating Floors: {self.bottomFloor}-{self.topFloor}")
     
def print_requests(): ###change and remove
    for x in range(len(requests)):
        print("Floor:", (x+1))
        print(requests[x])

def main(): ###change
    capacity = fileHandling(filename)[1]
    floors = fileHandling(filename)[2]
    lift = Lift(liftNumber=1,topFloor=floors,capacity=capacity)
    numofrequests = 1

    print_requests()
    while numofrequests != 0:
        switch = False
        
        lift.add_person()
        print(f"\nAdding People to Lift {lift.get_liftNumber()} ...\n")
        print_requests()
        print(lift)
        numof = input("")
        if ((lift.get_number_of_people() == 0 and not lift.checkAhead()) or lift.checkEnd()):
            switch = True

        lift.move_lift()
        if not switch:
            print(f"\nMoving Lift {lift.get_liftNumber()} ...\n")
        elif switch:
            print(f"\nLift {lift.get_liftNumber()} now going {lift.get_direction()} ...\n")
        print(lift)

    
        lift.remove_people()
        print(f"\nRemoving People from Lift {lift.get_liftNumber()} ...\n")
        print(lift)
        numof = input("")

        numofrequests = 0 + lift.get_number_of_people()
        for x in requests:
            numofrequests += len(x)

if __name__ == "__main__":
    main()