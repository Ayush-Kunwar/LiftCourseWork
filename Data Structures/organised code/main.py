from scan import scan
from look import look
from multipleLifts import customLift

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
    userInput = input("What lift progrom should run: ")
    inputSize = input("What size (small, medium, large): ")
    file = getSize(inputSize)
    if file:
        if userInput.lower() == "scan":
            scan(file)
        elif userInput.lower() == "look":
            look(file)
        elif userInput.lower() == "custom":
            customLift(file)