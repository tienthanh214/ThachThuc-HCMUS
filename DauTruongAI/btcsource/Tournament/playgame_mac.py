import json
import os
import random
import subprocess
import sys
from tqdm import tqdm
from subprocess import STDOUT, check_output
from copy import deepcopy 
import psutil

from _global import *
from _system import subprocess_args
from player import Player
from state import State
from utils import Vector2

players = [ Player(players_id[i], num_rows, num_cols) for i in range(2) ]

def get_next_move(t):
    moves = [ Vector2(0, 0) for i in range(2) ]
    for i in range(2):
        
        with open(f'{player_folders[players_id[i]]}/MAP.INP', 'w') as f:
            f.write(f'{num_rows} {num_cols} {num_moves - t}\n')
            f.write(f'{players[i].x} {players[i].y} {players[1-i].x} {players[1-i].y}\n')
            f.write(f'{players[i].point} {1 if players[i].shield else 0}\n')
            f.write('\n'.join([' '.join(x) for x in board]))
        
        output_path = f'{player_folders[players_id[i]]}/MOVE.OUT'
        open(output_path, 'w').close()

        try:
            # command = f'procgov64 -m 512M --cpu=1 -- {players_id[i]}.exe > log.txt'
            # command = f'python {players_id[i]}.py > log.txt'
            if os.path.exists(f'{player_folders[players_id[i]]}/{players_id[i]}.py'):
                command = f'python {players_id[i]}.py > log.txt'
            elif os.path.exists(f'./{player_folders[players_id[i]]}/{players_id[i]}'):
                command = f'./{players_id[i]} > log.txt'
            else:
                raise Exception(f'[{players_id[i]}][ERROR] No executable file found.')
            command = command.split()
            subprocess.check_call(command, timeout=2, cwd=f'{player_folders[players_id[i]]}', shell=True, **subprocess_args(False))
        except Exception as e:
            logger.append(str(e))

            PROC_NAME = [f"./{players_id[i]}", 'procgov64']

            for proc in psutil.process_iter():
                # check whether the process to kill name matches
                if proc.name() in PROC_NAME:
                    # proc.kill()
                    pass
        
        output_path = f'{player_folders[players_id[i]]}/MOVE.OUT'
        try:
            with open(output_path, 'r') as f:
                v = list(map(int, f.readline().split()))
                if len(v) == 2:
                    moves[i] = Vector2(*v)
                else: logger.append(f'[{players_id[i]}][ERROR] Invalid input file.')
        except Exception as e:
            logger.append(f'[{players_id[i]}][ERROR] {str(e)}')

    #     for i in range(2):
    #         folder = player_folders[players_id[i]] 
    #         item_ls = folder.glob('*')
    #         for item in item_ls:
    #             if item.is_file():
    #                 if item.name in ['MOVE.OUT', 'MAP.INP', 'STATE.OUT', 'log.txt']:
    #                     continue
    #                 elif item.name.endswith('.exe'):
    #                     continue
    #                 elif item.name.endswith('.py'):
    #                     continue
    #                 elif item.name.endswith('.dll'):
    #                     continue
    #                 else:
    #                     item.unlink()
    return moves
    
def check_valid(v):
    return 1 <= v.x <= num_rows and 1 <= v.y <= num_cols and board[v.x - 1][v.y - 1] == '0'

def get_random_vec(v):
    x = random.randint(1, num_rows)
    y = random.randint(1, num_cols)
    while not check_valid(Vector2(x, y)) or Vector2(x, y) == v:
        x = random.randint(1, num_rows)
        y = random.randint(1, num_cols)
    return x, y

def treasure_appear(total_moves, moveleft, p1, p2):
    # 1/2 total time (moveleft == 1/2 total moves)
    # treasure value = 3/4 abs(p1.point - p2.point)
    global treasure_appeared
    if not(treasure_appeared):
        if moveleft < 1/2 * total_moves and num_rows//2>0 and num_cols//2>0:
            treasure_appeared = True
            board[num_rows//2][num_cols//2] = str(max(int(3/4 * abs(p1.point - p2.point)),1))
            logger.append(f'Treasure appeared at ({num_rows//2+1}, {num_cols//2+1}). Treasure value = {board[num_rows//2][num_cols//2]}.')

def break_condition(total_init_coins, num_moves, moveleft, p1, p2):
    # 1/2 total time (moveleft == 1/2 total moves)
    # abs(p1.point - p2.point) > total available points / 5 
    if moveleft <= num_moves // 2:
        if abs(p1.point - p2.point) > total_init_coins // 5:
            logger.append(f'Break condition satisfied.')
            return True
    return False

def main():
    logger.append(f'[INFO] Step: 0, Remaining steps: {num_moves-1}/{num_moves}')
    for i in range(3):
        moves = get_next_move(0)
        if not(moves[0] == moves[1]):
            flag = True
            for i in range(2):
                if not check_valid(moves[i]):
                    logger.append(f'[{players_id[i]}] Invalid starting point {moves[i]}, retrying...')
                    moves[i] = Vector2(0, 0)
                    flag = False
            if flag:
                logger.append('Starting points are valid.')
            break
        else:    
            logger.append(f'[{players_id[0]}][{players_id[1]}] Coincided starting points {moves[0]}, {moves[1]}.')
    
    for i in range(2):
        if moves[i] == Vector2(0, 0):
            moves[i] = Vector2(*get_random_vec(Vector2(0, 0)))

    while moves[0] == moves[1]:
        logger.append(f'[{players_id[0]}][{players_id[1]}] Coincided starting points {moves[0]}, {moves[1]}.')
        moves[0] = Vector2(*get_random_vec(Vector2(0, 0)))
        moves[1] = Vector2(*get_random_vec(moves[0]))
    
    for i in range(2):
        logger.append(f'[{players_id[i]}] Starting point {moves[i]}.')
        players[i].set_pos(moves[i].x, moves[i].y)
    
    state = State.from_players(players[0], players[1], moveleft=num_moves-1, map=board)
    # outputs_stream.write(f'{state}\n')
    outputs_json[0] = state.to_dict()
    
    total_init_coins = 0
    for i in range(num_rows):
        for j in range(num_cols):
            if board[i][j].isdigit():
                total_init_coins += int(board[i][j])
    
    # outputs_stream.write(f'{players[0].x} {players[0].y} {players[1].x} {players[1].y}\n')
    for move_count in tqdm(range(1, num_moves)):
        logger.append(f'[INFO] Step: {move_count}, Remaining steps: {num_moves-move_count-1}/{num_moves}')
        treasure_appear(num_moves, num_moves-move_count-1, players[0], players[1])
        if break_condition(total_init_coins, num_moves, num_moves-move_count-1, players[0], players[1]):
            break
        moves = get_next_move(move_count)
        prev_pos = [ Vector2(p.x, p.y) for p in players ]
        for i in range(2):
            players[i].go(moves[i].x, moves[i].y)
        # outputs_stream.write(f'{players[0].x} {players[0].y} {players[1].x} {players[1].y}\n')
    
        if Vector2(players[0].x, players[0].y) == Vector2(players[1].x, players[1].y) \
            or (Vector2(players[0].x, players[0].y) == prev_pos[1] \
                and Vector2(players[1].x, players[1].y) == prev_pos[0]):
            players[0].die()
            players[1].die()

        for i in range(2):
            if players[i].alive:
                if board[players[i].x - 1][players[i].y - 1] == 'D':
                    players[i].encounter_trap()
                elif board[players[i].x - 1][players[i].y - 1] == 'S':
                    players[i].equip_shield()
                    board[players[i].x - 1][players[i].y - 1] = '0'
                elif board[players[i].x - 1][players[i].y - 1] != '0':
                    players[i].earn_point(int(board[players[i].x - 1][players[i].y - 1]))
                    board[players[i].x - 1][players[i].y - 1] = '0'
            
        state = State.from_players(players[0], players[1], moveleft=num_moves-move_count-1, map=board)
        # outputs_stream.write(f'{state}\n')
        tmp = deepcopy(state)
        outputs_json[move_count] = tmp.to_dict()
        if (not players[0].alive and not players[1].alive):
            logger.append(f'Both players died.')
            break

    logger.append('Final score:')
    for i in range(2):
        logger.append(f'[{players_id[i]}] is {"alive" if players[i].alive else "dead"}{" and shielded" if players[i].shield else ""} with {players[i].point} coins.')
    outputs_stream.writelines('\n'.join(logger))
    outputs_stream.close()
    # write json pretty indent
    with open(outputs_json_path, 'w') as f:
        json.dump(outputs_json, f, indent=4)

if __name__ == '__main__':
    main()
