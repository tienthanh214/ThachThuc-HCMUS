import csv

with open('TeamJazzyNew_TeamSenoNew_stat.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    cnt = 0
    fwin = 0
    fdraw = 0
    flose = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            cnt += 1
            if cnt == 1:
                map = row[0]
                win = 0
                draw = 0
                lose = 0
                score  = 0
            if row[5] > row[9]:
                status = "Win"
                win += 1
                score += int(row[5])
            elif row[5] == row[9]:
                status = "Draw"
                draw += 1
            else:
                status = "Lose"
                lose += 1
            if cnt == 10:
                cnt = 0
                print(map, win, draw, lose)
                fwin += win
                fdraw += draw
                flose += lose

print("Total:", fwin, fdraw, flose)
