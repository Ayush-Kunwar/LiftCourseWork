import re

is_numeric = lambda s: bool(re.fullmatch(r'\d+', s))

def fileHandling(filename):
    try:
        data = open(filename, "r") #open the text file
        lines = data.readlines()
        if len(lines) < 3:
            raise ValueError("ERROR: File is too short and is missing details")
        txt = lines[1].strip().replace(',','')
        if not txt.replace(" ","").isdigit():
            raise ValueError(f"ERROR: Number of Floors and Capacity is not defined properly")
        
        num = [int(s) for s in txt.split()]
        floors = num[0]
        capacity = num[1]
        
        if floors < 2:
            raise ValueError("ERROR: There must be at least 2 floors")
        if capacity < 1:
            raise ValueError("ERROR: Lift capacity must be atleast be 1")
        
        building = []
        for x in range(3, len(lines)):
            txt = lines[x].replace(',','')
            if not txt.strip().replace(":","").replace(" ","").isdigit():
                raise ValueError(f"ERROR: Invalid Floor Requests format")
            
            requests = [int(s) for s in txt.split() if s.isdigit()]
            current_floor = x - 2  # Since floors start from line 3, floor number is (x - 2)

            if any(request == current_floor for request in requests):
                raise ValueError(f"ERROR: Requested floor is the same as the current floor: {current_floor}")
            if any(request < 1 or request > floors for request in requests):
                raise ValueError(f"ERROR: Requested floor is out of building's range (floor: {current_floor})")
    
            building.append(requests)
        data.close()
        return building, capacity, floors
    
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found")
    
