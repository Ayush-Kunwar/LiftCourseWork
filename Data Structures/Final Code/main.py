from scan import scan
from look import look
from multipleLifts import customLift
from generatefiles import generateInput

def getSize(size):
    if size == "small":
        file = "input1.txt"
    elif size == "medium":
        file = "input2.txt"
    elif size == "large":
        file = "input3.txt"
    else:
        print("invalid size entered")
        return None
    return file

if __name__ == "__main__":
    userInput = input("What lift progrom should run (scan, look, custom): ")
    inputSize = input("What size (small, medium, large, custom): ")
    if inputSize == "custom": #custom input generated a new random file 
        floors = int(input("Enter number of floors: "))
        capacity = int(input("Enter lift capacity: "))
        requests = int(input("Enter number of request: "))
        generateInput("input1.txt", floors, capacity, requests)
        file = "input1.txt"
    else:
        file = getSize(inputSize)
    if file:
        if userInput.lower() == "scan":
            scan(file)
        elif userInput.lower() == "look":
            look(file)
        elif userInput.lower() == "custom":
            customLift(file)
        else:
            print("invalid size entered")