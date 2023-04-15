import random

def init_position(parsed_map):
    for i in range(len(parsed_map)):
        for j in range(len(parsed_map[i])):
            if parsed_map[i][j] == 0:
                return i+1, j+1

def parse_map(input_file):
    lines = input_file.read().splitlines()
    n, m, k = list(map(int, lines[0].strip().split(" "))) # n: number of rows, m: number of columns, k: number of steps
    x1, y1, x2, y2 = list(map(int, lines[1].strip().split(" "))) # (x1, y1): team position, (x2, y2): enemy position
    collected_gold, has_shield = list(map(int, lines[2].strip().split(" "))) # collected_gold: number of gold collected, has_shield: 1 if has shield, 0 otherwise
    parsed_map = lines[3:]
    for i, _ in enumerate(parsed_map):
        parsed_map[i] = parsed_map[i].strip().split(" ")

    for i in range(len(parsed_map)):
        for j in range(len(parsed_map[i])):
            if parsed_map[i][j].isdigit():
                parsed_map[i][j] = int(parsed_map[i][j])
    return n, m, k, x1, y1, x2, y2, collected_gold, has_shield, parsed_map

def logic(n, m, k, x1, y1, x2, y2, collected_gold, has_shield, parsed_map):
    if x1 == x2 == y1 == y2 == 0:
        return init_position(parsed_map)
    else:
        # move = random.choice(["LEFT", "RIGHT"])
        move = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        if move == "UP":
            return x1 - 1, y1
        elif move == "DOWN":
            return x1 + 1, y1
        elif move == "LEFT":
            return x1, y1 - 1
        elif move == "RIGHT":
            return x1, y1 + 1

def play(input_file, state_file, output_file):
    n, m, k, x1, y1, x2, y2, collected_gold, has_shield, parsed_map = parse_map(input_file)
    x1, y1 = logic(n, m, k, x1, y1, x2, y2, collected_gold, has_shield, parsed_map)
    print(x1, y1, file=output_file)

if __name__ == "__main__":
    input_file = open("MAP.INP", "r")
    state_file = open("STATE.OUT", "w")
    output_file = open("MOVE.OUT", "w")

    play(input_file, state_file, output_file)