import os

map = {
        "x1": 4,
        "y1": 10,
        "x2": 4,
        "y2": 7,
        "point1": 1,
        "shield1": True,
        "point2": 16,
        "shield2": False,
        "alive1": True,
        "alive2": True,
        "moveleft": 38,
        "map_humanreadable": [
            "D,0,2,1,0,0,0,0,0,0,1,0,D,0,0",
            "0,D,1,0,D,D,3,D,0,0,4,2,D,1,0",
            "2,1,D,2,0,2,0,0,4,3,0,0,0,1,0",
            "1,0,2,0,0,0,0,0,0,D,0,0,0,D,D",
            "0,D,0,0,0,0,0,D,0,0,0,1,0,0,1",
            "0,D,0,0,0,0,1,D,0,0,3,D,D,0,0",
            "0,0,0,0,0,1,0,D,0,1,0,D,1,0,0",
            "0,D,0,0,D,D,D,0,0,0,0,D,D,0,0",
            "0,0,4,1,0,0,0,0,0,D,1,0,1,0,1",
            "0,0,3,D,S,0,1,0,D,D,0,0,0,0,0",
            "1,4,0,0,0,3,0,0,1,0,D,1,0,1,0",
            "0,2,0,0,1,D,D,D,0,0,1,D,0,1,0",
            "D,D,0,0,0,D,1,D,1,0,0,0,0,0,D",
            "0,1,1,D,0,0,0,0,0,0,1,1,0,0,0",
            "0,0,0,D,1,0,0,0,1,0,0,0,D,0,5"
        ]
    }
# print(15, 15, map["moveleft"])
# print(map["x1"], map["y1"], map["x2"], map["y2"])
# print(map["point1"], int(map["shield1"]))
# for row in map["map_humanreadable"]:
#     rl = ""
#     for item in row.split(","):
#         rl += item + " "
#     print(rl)

strres = ""
maps = [1,2,3,4,5,6,7,8,9,10,15,21,23,26,27,28,31]
for map in maps:
    mapname = "Map" + str(map) + ".txt"
    if mapname == "Map1.txt":
        mapname = "Map.txt"
    f = open("./MapBK/" + mapname, "r")
    data = f.readlines()[1:]
    res = 0
    row = 0
    for datum in data:
        row += 1
        items = datum.split()
        col = 0
        for item in items:
            col += 1
            if item == "D":
                res = res * 301 + row * 17 + col
                res %= 1000000007
    # print(map, res)
    strres += str(res) + ","
print(strres)