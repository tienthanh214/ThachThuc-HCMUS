file = open('output.txt', 'r')

lines = file.readlines()

hasDone = True
for i in range(0, len(lines), 2):
    st = lines[i][:-1]
    K = int(lines[i + 1])
    
    binStr = ''
    for c in st:
        binStr += (bin(ord(c))[3:])

    for i in range(0, len(binStr), 8):
        cur = int(binStr[i : i + 8], 2) ^ K
        print(chr(cur), end = '')
    print('\n')

        