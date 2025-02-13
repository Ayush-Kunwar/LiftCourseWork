import re

is_numeric = lambda s: bool(re.fullmatch(r'\d+', s))

def fileHandling(filename = "data.txt"):
    data = open("data.txt", "r")
    lines = data.readlines()

    txt = lines[1].replace(',','')
    num = [int(s) for s in txt.split() if s.isdigit()]
    floors = num[0]
    capacity = num[1]

    building = []
    for x in range(3, len(lines)):
        txt = lines[x].replace(',','')
        requests = [int(s) for s in txt.split() if s.isdigit()]
        building.append(requests)
    print(building)

if __name__ == "__main__":
    fileHandling()