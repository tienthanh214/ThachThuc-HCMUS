from pathlib import Path
import sys 
import json
from argparse import ArgumentParser 
logger = []

def get_args():
    parser = ArgumentParser()
    parser.add_argument('--map', type=str, default='map1', help='map path')
    parser.add_argument('--player1', type=str, default='player1', help='player1 folder path')
    parser.add_argument('--player2', type=str, default='player2', help='player2 folder path')
    parser.add_argument('--output', type=str, default='Match', help='match log output folder path')
    return parser.parse_args()

args = get_args()

assert Path(args.map).exists(), f'{args.map} does not exist'
assert Path(args.player1).exists(), f'{args.player1} does not exist'
assert Path(args.player2).exists(), f'{args.player2} does not exist'
if not Path(args.output).exists():
    Path(args.output).mkdir()

map_file = open(args.map)
players_id = [Path(args.player1).stem, Path(args.player2).stem]
match_filename = f'{players_id[0]}_{players_id[1]}_{Path(args.map).stem}'
outputs_json_path = f'{args.output}/{match_filename}.json'
outputs_stream = open(f'{args.output}/{match_filename}.txt', 'w')

player_folders = {players_id[0]: Path(args.player1), players_id[1]: Path(args.player2)}

# root = sys.argv[1]
# player_sub = 'Players'
# match_sub = 'Match'
# map_sub = 'Maps'
# map_id = sys.argv[2]
# players_id = sys.argv[3:5]

# map_file = open(f'{root}/{map_sub}/{map_id}.txt')
# outputs_json_path = f'{root}/{match_sub}/{players_id[0]}_{players_id[1]}_{map_id}.json'
# outputs_stream = open(f'{root}/{match_sub}/{players_id[0]}_{players_id[1]}_{map_id}.txt', 'w')



num_rows, num_cols, num_moves = map(int, map_file.readline().strip().split())
board = [x.strip().split(' ') for x in map_file.readlines()]
outputs_json = {}
treasure_appeared = False

