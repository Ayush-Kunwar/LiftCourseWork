from fileHandling import fileHandle

class Person:
    def __init__(self, floor, destination):
        self.floor = floor
        self.destination = destination

    def checkDestination(self, currentFloor):
        return self.destination == currentFloor

class Lift:
    def __init__(self, capacity, floors):
        self.capacity = capacity
        self.floors = floors
        self.currentFloor = 1
        self.currentLift = []
        self.direction = "up"

    def checkDirection(self, person):
        """Determine if the person is going in the same direction as the lift."""
        return "up" if person.destination > self.currentFloor else "down"

    def load(self, persons):
        """Load only the people at the current floor in the same direction."""
        remaining_persons = []
        new_passengers = []

        for person in persons:
            if person.floor == self.currentFloor and self.isRoom():
                if self.checkDirection(person) == self.direction:
                    new_passengers.append(person)
                else:
                    remaining_persons.append(person)  # Collect valid passengers at the current floor
            else:
                remaining_persons.append(person)  # Keep those who can't board

        self.currentLift.extend(new_passengers)  # Add new passengers to lift
        return remaining_persons  # Return only people who are still waiting

    def unload(self):
        """Safely remove passengers at their destination without skipping elements."""
        self.currentLift = [p for p in self.currentLift if p.destination != self.currentFloor]

    def checkTop(self):
            return self.currentFloor == self.floors

    def checkBottom(self):
            return self.currentFloor == 1

    def move(self):
        """Move the lift up or down based on direction."""
        if self.direction == "up" and self.currentFloor < self.floors and checkAhead(self, []):
            self.currentFloor += 1
            if self.checkTop():
                self.changeDirection()

        elif self.direction == "down" and self.currentFloor > 1 and checkAhead(self, []):
            self.currentFloor -= 1
            if self.checkBottom():
                self.changeDirection()


    def changeDirection(self):
        """Switch direction of the lift."""
        self.direction = "down" if self.direction == "up" else "up"

    def isRoom(self):
        """Check if there is room in the lift."""
        return len(self.currentLift) < self.capacity

def checkAhead(lift, persons):
    """Check if there are valid requests ahead in the current direction."""
    if lift.direction == "up":
        return any(person.floor > lift.currentFloor or person.destination > lift.currentFloor for person in persons + lift.currentLift)
    elif lift.direction == "down":
        return any(person.floor < lift.currentFloor or person.destination < lift.currentFloor for person in persons + lift.currentLift)
    return False


def checkLift(lift):
    """Check if there are still destinations in the current direction."""
    if lift.direction == "up":
        return any(person.destination > lift.currentFloor for person in lift.currentLift)
    elif lift.direction == "down":
        return any(person.destination < lift.currentFloor for person in lift.currentLift)
    return False

def loadPersons(requests):
    """Convert the list of requests into individual objects."""
    requestsAsClass = []
    for i in range(len(requests)): #for each floor
        for j in range(len(requests[i])): #for each person
            person = Person(i+1, requests[i][j]) #make them a Person with current floor and destination as attributes
            requestsAsClass.append(person) #add to list
    return requestsAsClass


def LOOK(lift, persons, maxFloor):
    """SCAN Algorithm: Moves in one direction until no requests exist ahead."""
    while persons or lift.currentLift  :  # Only continue if people are waiting or inside lift
        lift.unload()  # Drop off passengers
        persons = lift.load(persons)  # Load waiting passengers
        print(f"Lift is at floor {lift.currentFloor}, direction: {lift.direction} currentLift: {[p.destination for p in lift.currentLift]}")

        # ✅ Stop condition: No one in lift and no pending requests
        if lift.currentFloor == 12:
            break
        if not checkAhead(lift, persons) and not checkLift(lift) and not(lift.checkTop() and lift.checkBottom()):
            lift.changeDirection()
        
        if not checkAhead(lift, persons) and not checkLift(lift):
            break  # Exit the loop when all requests are completed

        # ✅ Change direction BEFORE moving


        lift.move()
        #print(f"Lift is direction: {lift.direction} currentLift:")
    print("✅ Lift is empty, and no more people are waiting!")


def main():
    requests, capacity, floors = fileHandle(r"Data Structures\input1.txt")  # Load data
    lift = Lift(capacity, floors)  # Create lift object
    persons = loadPersons(requests)  # Get the list of people objects
    LOOK(lift, persons, floors)

if __name__ == "__main__":
    main()
