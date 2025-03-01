from fileHandling import fileHandling
from request import loadRequests, print_requests
from lift import Lift


def lift_setup(filename, numberOfLifts: int = 1):
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

def customLift(filename):
    requests = loadRequests(filename)
    numofrequests = 1
    floors = fileHandling(filename)[2]
    numberOfLifts = 0
    exit = False
    passes = 0
    #states = ["add", "move", "remove", "idle"]

    while numberOfLifts < 1:
        numberOfLifts = int(input(f"\nHow many lifts would you like in your {floors} story building?\033[0m\n"))
    lifts = lift_setup(filename, numberOfLifts = numberOfLifts)

    print_requests(requests)
    while numofrequests != 0 and not exit:
        exit = False
        noRemove = False
        for lift in lifts:
            """Removes people from the lift"""
            if lift.get_state() == "remove": #remove only if there are people to remove 
                noRemove = False
                peopleBefore = lift.get_number_of_people()
                requests = lift.remove_people(requests)
                if not peopleBefore == lift.get_number_of_people():
                    print(f"\n\033[1mRemoving People from Lift {lift.get_liftNumber()} ...\033[0m\n")
                    if lift.checkEnd():
                        print_requests(requests)
                    print(lift)
                    if ((lift.get_number_of_people() == 0 and not lift.checkAhead(requests)) or lift.checkEnd()): #change direction
                        lift.set_state("move")
                    else: 
                        lift.set_state("add")
                elif ((lift.get_number_of_people() == 0 and not lift.checkAhead(requests)) or lift.checkEnd()): #change direction
                    lift.set_state("move")
                else:
                    noRemove = True
                    lift.set_state("add")
                
            """Check if has no requests to respond to"""
            if lift.checkNoRequests(requests):
                lift.set_state("idle")

                """Moves the lift/Change direction of the lift"""
            if lift.get_state() == "move":
                if ((lift.get_number_of_people() == 0 and not lift.checkAhead(requests)) or lift.checkEnd()): #check to see if the lift is changing direction instead of moving
                    lift.move_lift(requests)
                    print(f"\n\033[1mLift {lift.get_liftNumber()} now going {lift.get_direction()} ...\033[0m\n")
                    print(lift)
                    lift.set_state("add")
                else: 
                    lift.move_lift(requests)
                    print(f"\n\033[1mMoving Lift {lift.get_liftNumber()} ...\033[0m\n")
                    print(lift)
                    lift.set_state("remove")
                
                """Adds people to the lift"""
            if lift.get_state() == "add": #add only if there are people to add
                peopleBefore = lift.get_number_of_people()
                requests = lift.add_person(requests)
                if not peopleBefore == lift.get_number_of_people():        
                    print(f"\n\033[1mAdding People to Lift {lift.get_liftNumber()} ...\033[0m\n")
                    print_requests(requests)
                    print(lift)
                    lift.set_state("move")
                elif noRemove or passes == 0: #moving lift if the lift doesn't add or remove people
                    lift.move_lift(requests)
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
                    print_requests(requests)
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
                        print_requests(requests)
                        pause = input("\n\033[1mType 'e' to Exit.\nPress Enter to continue.\n\033[0m")
                if pause.lower() == "e":
                    exit = True
                lift.set_state("remove")
            
            """Pause for the simulation"""
            if not lift.checkNoRequests(requests):
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
