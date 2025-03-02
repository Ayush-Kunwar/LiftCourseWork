from fileHandling import fileHandling
from request import loadRequests, print_requests
from lift import Lift


def scan(filename):
    requests = loadRequests(filename)
    capacity = fileHandling(filename)[1]
    numofrequests = 1
    floors = fileHandling(filename)[2]

    passes = 0
    switch = False
    lift = Lift(liftNumber = 1, topFloor = floors, capacity = capacity)

    print_requests(requests)
    while numofrequests != 0 :
        requests = lift.add_person(requests)
        print(f"\n\033[1mAdding People to Lift {lift.get_liftNumber()} ...\033[0m\n")
        print_requests(requests)
        print(lift)

        if lift.checkEnd():
            switch = True
        else:
            switch = False
        lift.move_lift_scan()
        lift.update_waiting_times(requests) 
        lift.update_travel_times()   
        if not switch:
            print(f"\nMoving Lift {lift.get_liftNumber()} ...\n")
        elif switch:
            print(f"\nLift {lift.get_liftNumber()} now going {lift.get_direction()} ...\n")
        print(lift)

        requests = lift.remove_people(requests)  # Unload passengers who reached their destination
        print(f"\n\033[1mRemoving People from Lift {lift.get_liftNumber()} ...\033[0m\n")
        print_requests(requests)
        print(lift)

        #pause = input("\nPress Enter to continue.\n")
        print("\n\033[1m----------------------------------------\033[0m\n") #1 time has passed
        passes += 1
    

        numofrequests = 0
        numofrequests += lift.get_number_of_people()
        for x in requests:
            numofrequests += len(x)
    lift.statistics.generate_statistics()
    lift.statistics.plot_statistics()
    print("Passes: ", passes)
    print("\n\033[1mSimulation Finished\n\033[0m")
scan("input1.txt")
