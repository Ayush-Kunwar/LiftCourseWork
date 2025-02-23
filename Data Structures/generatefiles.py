import random

def generateInput(name, floors, capacity, totalRequests):
    file =  open(name, "w")
    file.write("# Number of Floors, Capacity\n")
    file.write(f"{floors}, {capacity}\n")
    file.write("# Floor Requests\n")

    remRequests = totalRequests # Variable to distribute requests in the building
    exRequests = [0] * floors  # Initiliase array to keep track of amount of requests on each floor

    while remRequests > 0: # Distribute the requests amongst the floors
        floor = random.randint(1, floors)  
        destination = random.randint(1, floors) # Randomly assign how many reuests each floor will have

        if destination != floor:  # Make sure the request is valid
            exRequests[floor - 1] += 1  # Increment the amount of requests to be placed on that floor
            remRequests -= 1      

    # Put requests in the file
    for floor in range(1, floors + 1):
        if exRequests[floor - 1] > 0:
            destinations = set() # Make sure no duplicates
            for i in range(exRequests[floor - 1]):
                destination = random.randint(1, floors)
                while destination == floor: # Reroll request if invalid
                    destination = random.randint(1, floors) 
                destinations.add(destination)
            if floor == 1:   # Ensure theres no blank lines in file
                file.write(f"{floor}: {', '.join(map(str, destinations))}")
            else:
                file.write(f"\n{floor}: {', '.join(map(str, destinations))}")

        else:
            if floor == 1: # Ensure theres no blank lines in file
                file.write(f"{floor}:")
            else:
                file.write(f"\n{floor}:")
          


    file.close()

generateInput("in1.txt", floors=10, capacity=4, totalRequests=20)
generateInput("in2.txt", floors=15, capacity=7, totalRequests=30)
generateInput("in3.txt", floors=20, capacity=8, totalRequests=40)