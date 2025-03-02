from fileHandling import fileHandling
from request import loadRequests, print_requests
from lift import Lift

def look(filename):
    requests = loadRequests(filename)
    capacity = fileHandling(filename)[1]
    numofrequests = 1
    floors = fileHandling(filename)[2]
    passes = 0
    exit = False

    lift = Lift(liftNumber = 1, topFloor = floors, capacity = capacity)

    print_requests(requests)
    while numofrequests != 0 and not exit:
        exit = False
        if not lift.checkNoRequests(requests):
            switch = False
            if not lift.checkEnd():
                """Adds people to the lift"""
                requests = lift.add_person(requests)
                print(f"\nAdding People to Lift {lift.get_liftNumber()} ...\n")
                print_requests(requests)
                print(lift)
                #pause = input("\nPress Enter to continue.\n")
            
            if ((lift.get_number_of_people() == 0 and not lift.checkAhead(requests)) or lift.checkEnd()):
                switch = True

            """Moves the lift/Change direction of the lift"""
            lift.move_lift(requests)
            lift.update_waiting_times(requests) 
            lift.update_travel_times()
            if not switch:
                print(f"\nMoving Lift {lift.get_liftNumber()} ...\n")
            elif switch:
                print(f"\nLift {lift.get_liftNumber()} now going {lift.get_direction()} ...\n")
            print(lift)

            """Removes people from the lift"""
            requests = lift.remove_people(requests)
            print(f"\nRemoving People from Lift {lift.get_liftNumber()} ...\n")
            print_requests(requests)
            print(lift)
            #pause = input("\nPress Enter to continue.\n")

        else:
            pause = ""
            print(f"\nLift {lift.get_liftNumber()} has no requests.\n")
            pause = input("\nType 'b' to See All Requests.\nType 'e' to Exit.\nPress Enter to continue.\n")
            if pause.lower() == "b":
                print_requests(requests)
            elif pause.lower() == "e":
                exit = True

        print("\n----------------------------------------\n")

        numofrequests = 0
        numofrequests += lift.get_number_of_people()
        passes += 1
        

        for x in requests:
            numofrequests += len(x)
        
    lift.statistics.generate_statistics()
    lift.statistics.plot_statistics()
    print("Passes: ", passes)
    print("\n\033[1mSimulation Finished\n\033[0m")

look("input1.txt")
