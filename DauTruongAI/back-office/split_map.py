import os

def split_map(filename, K):
    curpath = os.path.join(os.getcwd())

    dir = filename.split('.')[0]
    if not os.path.exists(os.path.join(curpath, dir)):
        os.mkdir(os.path.join(curpath, dir))

    with open(os.path.join(curpath, filename), "r") as inputfileobject:
        for line in inputfileobject:
            items = line.split()
            if len(items) == 0:
                continue
            if len(items) == 1:
                output_file = os.path.join(curpath, dir, items[0])
                output_file_object = open(output_file, "w")
            if len(items) == 2:
                output_file_object.write(items[0] + " " + items[1] + " " + str(K) + "\n")
                # output_file_object.write("0 0 0 0\n")
                # output_file_object.write("0 0\n")
            if len(items) > 2:
                output_file_object.write(line)



split_map("MapBK.txt", 50)
