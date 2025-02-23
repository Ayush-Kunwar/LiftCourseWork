from fileHandling import fileHandling

class Person:
    def __init__(self, floor, destination):
        self.floor = floor
        self.destination = destination
    def checkDestination(self, currentFloor): #check if person has reached their destination
        if self.destination == currentFloor:
            return True
        else:
            return False

class Lift:
    def __init__(self, capacity, floors):
        self.capacity = capacity
        self.floors = floors
        self.currentFloor = 1
        self.content = []

    def load(self, persons):
        '''
        loop through each person
        check if there is room in lift and  see if they are on the same floor as the lift
            if they are add them to lift
        if not
            add them to a remaing person lift
        return the lift
        '''
        remaining_persons = []  # List to store persons who couldn't be loaded
        for person in persons:
            if person.floor == self.currentFloor and self.isRoom():  # Check if person is at the current floor and there is room
                self.content.append(person)  # add person to lift
            else:
                remaining_persons.append(person)  # keep person in waiting list
        return remaining_persons

    def isRoom(self): #check if there is room in lift 
        if len(self.content) < self.capacity:
            return True
        else:
            return False
    
    def unload(self):

        #for person in (self.content): #check everyone in the lift
            #if person.destination == self.currentFloor: #check if the current floor is their destination
                #self.content.remove(person) #remove them from the lift 
        
        self.content = [person for person in self.content if person.destination != self.currentFloor] # updated unload function as
        # old function had risks arising from iterating over and removing variables from a list.


def loadPersons(requests): #convert the list of requests into individual objects
    requestsAsClass = []
    for i in range(len(requests)): #for each floor
        for j in range(len(requests[i])): #for each person
            person = Person(i+1, requests[i][j]) #make them a Person with current floor and destination as attributes
            requestsAsClass.append(person) #add to list
    return requestsAsClass

def checkDirection(currentDirection, currentFloor, maxFloor): #check if we have reached top or bottom then reverse direction
    if currentDirection == "right":
        if currentFloor < maxFloor: #if we are going right (up)
            currentFloor += 1
        else: #if we are at the max floor start going left
            currentDirection = "left"
            currentFloor -= 1
    elif currentDirection == "left":
        if currentFloor > 1: #if we are going left (down)
            currentFloor -= 1
        else: #if we are at the bottom floor
            currentDirection = "right"
            currentFloor += 1 #fix: ensure the lift moves up a floor after changing direction
            
    return currentDirection, currentFloor


def SCAN(lift, persons, maxFloor):
    '''
    want to loop through all people and until lift is empty
    while its moving up (right) 
        check if lift has room
            if does
                check if anyone at the current floor
                add them to lift
                remove them from waiting to join lift
            increase floor by 1

    '''
    direction = "right"  # Default direction
    floor = 1  # Default floor
    previous_count = -1  # Track previous lift occupancy

    while len(persons) > 0 or len(lift.content) > 0:  # Continue until lift is empty and no one is waiting
        lift.unload()  # Unload passengers who reached their destination
        persons = lift.load(persons)  # Load new passengers

        if len(lift.content) == previous_count and not persons:  # If no changes, end loop
            break
        previous_count = len(lift.content)  # Update previous count

        print(f"Lift is at floor {lift.currentFloor}, content: {[person.destination for person in lift.content]}")
        direction, floor = checkDirection(direction, floor, maxFloor)  # Update direction
        lift.currentFloor = floor  # Move lift

    print("Lift is Empty and no more people waiting")

def main():
    requests, capacity, floors = fileHandling("input3.txt") #load data
    lift = Lift(capacity, floors) #create lift object
    persons = loadPersons(requests) #get the list of people objects
    SCAN(lift, persons, floors)

if __name__ == "__main__":
    main()