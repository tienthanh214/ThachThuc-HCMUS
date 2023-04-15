import csv

# with open('TeamThanh_TeamTrucJ_stat (1).csv') as csv_file:
with open('TeamThanh_TeamJazzy_stat.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    cnt = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            cnt += 1
            if cnt == 1:
                map = row[0]
                win = 0
                score  = 0
            if row[5] > row[9]:
                status = "Win"
                win += 2
                score += int(row[5])
            elif row[5] == row[9]:
                status = "Draw"
                win += 1
            else:
                status = "Lose"
            if cnt == 10:
                cnt = 0
                print(map, win, score)
