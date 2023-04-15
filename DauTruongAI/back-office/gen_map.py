from enum import Enum
from random import randint, randrange, random
import os


# Config

ratio_horizontal = 1
ratio_vertical = 1
ratio_main_diagonal = 1
ratio_sub_diagonal = 1
# Tỉ lệ random trục đối xứng, ví dụ như trên thì tỉ lệ các trục đối xứng là như nhau

ratio15 = 5
ratio13 = 3
ratio11 = 2
# Tỉ lệ random cạnh 15, 13, 11, ví dụ như trên thì tỉ lệ chọn cạnh 15 là: 5/(5+3+2)

ratio_gold = [13,11,9,5,2]
# Tỉ lệ random giá trị vàng trong ô, lần lượt là 1 2 3 4 5, ví dụ như trên thì tỉ lệ chọn giá trị 2 là 11/(13+11+9+5+2)

num_of_map = 30
# Số lượng map muốn gene

save_path = "./generated_map"
# Folder lưu map



class Axis(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    MAIN_DIAGONAL = 3
    SUB_DIAGONAL = 4

# Thuật toán dưới đây generate map dựa theo 2 trục: đường chéo chính và trục tung.
# (Các trục khác sẽ được sinh bằng cách sinh theo trục tương tự rồi lấy đối xứng).
# Thuật toán sinh map theo thứ tự:
#       - Sinh các ô D trên 1 nửa map
#       - Sinh các ô S trên 1 nửa map
#       - Sinh các ô gold trên 1 nửa map
#       - Lấy đối xứng qua trục để có nửa map còn lại
def gene_map(M:int, N:int, axis:Axis, dangerous_cnt:int):
    def is_diagonal() -> bool:
        return axis == Axis.MAIN_DIAGONAL or axis == Axis.SUB_DIAGONAL
    def is_in_axis(x:int, y:int) -> bool:
        if is_diagonal():
            if x == y:
                return True
        else:
            if y*2 == N+1:
                return True
        return False
        
    # Lưu các ô xung quanh
    around = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

    # Để tạo thành đồ thị liên thông giữa các ô không phải D, thì các ô D phải tạo thành đồ thị không có chu trình (hoặc chu trình này không chứa ô trống nào ở giữa).
    # Thuật toán dưới đây sinh D vừa trên điều kiện như trên, và sinh đến khi nào đủ dangerous_cnt
    # Chi tiết hơn:
    #       Đồ thị các ô D toạ thành các thành phần liên thông, mỗi thành phần liên thông KHÔNG chứa ô trống nào
    #       Lưu lại index cho từng thành phần liên thông
    #       Nếu thêm 1 ô D làm cho 2 thành phần liên thông nối lại với nhau, thì đánh lại index cho cả 2 thành phần đó
    #       Nếu thêm 1 ô D làm cho 1 thành phần liên thông nào đó tạo thành chu trình ==>> không được thêm ô D đó

    # Tinh chỉnh M, N, dưới đây chỉ gene map theo trục tung và đường chéo chính.
    if axis == Axis.HORIZONTAL:
        M, N = N, M
    elif is_diagonal():
        N = M

    # Khởi tạo map và mảng lưu chỉ số của các đồ thị liên thông
    map = [["0"]*(N+2) for _ in range(M+2)]
    connected_ids = [[-1]*(N+2) for _ in range(M+2)]
    connected_id_cnt = 0

    if is_diagonal():
        for i in range(M+1):
            map[i][0] = 'X'
            map[M+1][i+1] = 'X'
            map[i][i+1] = 'X'
            connected_ids[i][0] = 0
            connected_ids[M+1][i+1] = 0
            connected_ids[i][i+1] = 0
    else:
        for i in range(M+2):
            map[i][0] = 'X'
            map[i][(N+3)//2] = 'X'
            connected_ids[i][0] = 0
            connected_ids[i][(N+3)//2] = 0
        for i in range((N+3)//2):
            map[0][i] = 'X'
            map[M+1][i] = 'X'
            connected_ids[0][i] = 0
            connected_ids[M+1][i] = 0

    
    loop_cnt = 100 # Tránh lặp quá nhiều lần
    while loop_cnt > 0 and dangerous_cnt > 0:
        loop_cnt -= 1
        x, y = randint(1,M) , randint(1,N+1)
        if is_diagonal():
            if x < y:
                x, y = y-1, x
        else:
            if y*2 > N+1:
                y = N+1 - y
        if x == (M+1)/2 and y == (N+1)/2:
            continue
        if map[x][y] == 'D':
            continue
        
        validated = True
        id_around = set()
        visited = [False]*8
        for id in range(8):
            i, j = around[id]
            connected_id = connected_ids[x+i][y+j]
            if connected_id >= 0:
                if connected_id in id_around:
                    if visited[id]:
                        continue
                    validated = False

                id_around.add(connected_id)

                visited[id] = True
                stack = [id]
                while len(stack) > 0:
                    uid = stack.pop()
                    neighbor_id = [uid+7, uid+1]
                    if uid % 2 == 1:
                        neighbor_id = [uid+8, uid+7, uid+1, uid+2]
                    for vid in neighbor_id:
                        if vid >= 8:
                            vid -= 8
                        vi, vj = around[vid]
                        if connected_ids[x+vi][y+vj] == connected_ids[x+i][y+j] and not visited[vid]:
                            visited[vid] = True
                            stack.append(vid)
                    
        if not validated:
            continue

        map[x][y] = 'D'
        if is_in_axis(x,y):
            dangerous_cnt -= 1
        else:
            dangerous_cnt -= 2


        if len(id_around) == 0:
            connected_id_cnt += 1
            connected_ids[x][y] = connected_id_cnt
            continue
        
        cur_id = min(id_around)
        connected_ids[x][y] = cur_id
        for i in range(M+2):
            for j in range(N+2):
                for id in id_around:
                    if connected_ids[i][j] == id:
                        connected_ids[i][j] = cur_id

    if axis == Axis.MAIN_DIAGONAL or axis == Axis.SUB_DIAGONAL:
        for x in range(0,M+2):
            for y in range(0,N+2):
                if x < y:
                    map[x][y] = map[y][x]
    else:
        for x in range(0,M+2):
            for y in range((N+1)//2, N+2):
                map[x][y] = map[x][N+1-y]
                

    # gene shield
    while True:
        x, y = randint(1,M) , randint(1,N+1)
        if is_diagonal():
            if x < y:
                x, y = y-1, x
        else:
            if y*2 > N+1:
                y = N+1 - y
        if map[x][y] == 'D':
            continue
        if x == (M+1)/2 and y == (N+1)/2:
            continue
        
        map[x][y] = 'S'
        if not is_in_axis(x,y):
            if is_diagonal():
                map[y][x] = 'S'
            else:
                map[x][N+1-y] = 'S'
            break
        
        blank_center_cells = list()
        for i in range(1, M+1):
            if i*2 == M+1:
                continue
            if is_diagonal():
                if map[i][i] == '0':
                    blank_center_cells.append((i,i))
            else:
                if map[i][(N+1)//2] == '0':
                    blank_center_cells.append((i,(N+1)//2))
        if len(blank_center_cells) == 0:
            map[x][y] = '0'
            continue
        rd = randrange(0,len(blank_center_cells))
        x, y = blank_center_cells[rd]
        map[x][y] = 'S'
        break


    # gene gold
    def weight(pair):
        # Hàm này để tính trọng số khi gene vàng, trọng số càng cao thì ô đó càng dễ có vàng
        (x,y) = pair
        score = max(M,N)
        for (i,j) in [(-1,0),(0,1),(1,0),(0,-1)]:
            if map[x+i][y+j] == 'X':
                score += 2
            elif map[x+i][y+j] == 'D':
                score += 1
        return score * random()
    blank_cells = list()
    for x in range(1,M+1):
        for y in range(1,N+1):
            if x*2 == M+1 and y*2 == N+1:
                continue
            if map[x][y] == '0':
                blank_cells.append((x,y))
    blank_cells = sorted(blank_cells, reverse = True, key = weight)

    total_gold = 100
    cell_id = 0
    sum_ratio = sum(ratio_gold)
    while total_gold > 0:
        if cell_id == len(blank_cells):
            cell_id = 0
        x,y = blank_cells[cell_id]

        rd = randint(1,sum_ratio)
        gold = 1
        for rs in ratio_gold:
            if rd <= rs:
                break
            gold += 1
            rd -= rs

        base_gold = int(map[x][y])
        gold = min(gold + base_gold, 5)

        if is_in_axis(x,y):
            gold = min(gold - base_gold, total_gold) + base_gold
            total_gold -= gold - base_gold
            map[x][y] = str(gold)
            cell_id += 1
            pre_axis_cell = (x,y)
            continue
        gold = min(gold - base_gold, total_gold // 2) + base_gold
        total_gold -= (gold - base_gold) * 2
        map[x][y] = str(gold)
        if is_diagonal():
            map[y][x] = str(gold)
        else:
            map[x][N+1-y] = str(gold)
        cell_id += 1

        if total_gold == 1:
            (x,y) = pre_axis_cell
            gold = int(map[x][y])
            if gold < 5:
                map[x][y] = str(gold+1)
                break
            map[x][y] = '0'
            total_gold += 5



    if axis == Axis.SUB_DIAGONAL:
        newmap = [["0"]*(N+2) for _ in range(M+2)]
        for x in range(0,M+2):
            for y in range(0,N+2):
                newmap[x][y] = map[x][N+1-y]
        return newmap

    if axis == Axis.HORIZONTAL:
        M, N = N, M
        newmap = [["0"]*(N+2) for _ in range(M+2)]
        for x in range(0,M+2):
            for y in range(0,N+2):
                newmap[x][y] = map[y][x]
        return newmap

    return map


def rand_edge_len():
    rd = randint(1,ratio15 + ratio13 + ratio11)
    if rd <= ratio15:
        return 15
    elif rd <= ratio15 + ratio13:
        return 13
    else:
        return 11

def rand_axis() -> Axis:
    rd = randint(1, ratio_horizontal + ratio_vertical + ratio_main_diagonal + ratio_sub_diagonal)
    if rd <= ratio_horizontal:
        return Axis.HORIZONTAL
    elif rd <= ratio_horizontal + ratio_vertical:
        return Axis.VERTICAL
    elif rd <= ratio_horizontal + ratio_vertical + ratio_main_diagonal:
        return Axis.MAIN_DIAGONAL
    else:
        return Axis.SUB_DIAGONAL

for id in range(num_of_map):
    rd_axis = rand_axis()
    if rd_axis == Axis.MAIN_DIAGONAL or rd_axis == Axis.SUB_DIAGONAL:
        M = rand_edge_len()
        N = M
    else:
        M = rand_edge_len()
        N = rand_edge_len()
    dangerous_cnt=randint(int(M*N/5)-5, int(M*N/4.5))

    map = gene_map(M, N, rd_axis, dangerous_cnt)

    with open(os.path.join(save_path,f"map{id+1}.txt"), "w") as f:
        f.write(str(M) + " " + str(N) + "\n")
        for x in range(1,M+1):
            line = ""
            for y in range(1,N+1):
                line += map[x][y] + " "
            line += "\n"
            f.write(line)
