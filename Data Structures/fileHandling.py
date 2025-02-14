def fileHandling(filename = "data.txt"):
    data = open("data.txt", "r")
    lines = data.readlines()
    data.close()

    txt = lines[1].replace(',','')
    num = [int(s) for s in txt.split() if s.isdigit()]
    floors = num[0]
    capacity = num[1]

    building = []
    for x in range(3, len(lines)):
        txt = lines[x].replace(',','')
        txt = txt.strip("\n")
        requests = [int(s) for s in txt.split() if s.isdigit()]
        building.append(requests)

if __name__ == "__main__":
    fileHandling()
