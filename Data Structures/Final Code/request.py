from fileHandling import fileHandling
from person import Person

def loadRequests(filename = "input1.txt"): #convert the list of requests into individual objects
    requests = fileHandling(filename)[0]
    requestsAsClass = []
    for i in range(len(requests)): #for each floor
        floor = []
        for j in range(len(requests[i])): #for each person
            person = Person(i+1, requests[i][j]) #make them a Person with current floor and destination as attributes
            floor.append(person) #add to list
        requestsAsClass.append(floor)
    return requestsAsClass

def print_requests(requests):
    print("\n\033[1m\033[4mAll Requests\033[0m")
    for x in range(len(requests)):
        print(f"Floor: {x + 1}")
        print("\033[2m" ,requests[x], "\033[0m")

