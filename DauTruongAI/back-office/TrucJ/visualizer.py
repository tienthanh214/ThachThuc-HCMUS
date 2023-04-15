import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
import copy

root = os.path.join(os.getcwd(), "TrucJ")
src_dir = "CellScore"
dest_dir = "CellScoreVis"
src_dir = os.path.join(root, src_dir)
dest_dir = os.path.join(root, dest_dir)
os.makedirs(dest_dir, exist_ok=True)


def gen_vis(map, annot, save_path):
    # create a heatmap of the data
    plt.clf()
    sns.heatmap(map, vmin=0)
    plt.savefig(save_path)


for map_filename in tqdm(os.listdir(src_dir)):
    lines = None

    with open(os.path.join(src_dir, map_filename), "r") as f:
        lines = f.readlines()
    M, N = list(map(int, lines[0].split(" ")))

    parsed_map = lines[1:]
    for i, _ in enumerate(parsed_map):
        parsed_map[i] = parsed_map[i].strip().split(" ")

    annot_map = copy.deepcopy(parsed_map)
    sum = 0
    for i in range(M):
        for j in range(N):
            parsed_map[i][j] = float(parsed_map[i][j])
            sum += parsed_map[i][j]
    if sum != 100:
        print(f"{map_filename} value sum does not equal 100. Calculated value {sum}!")

    img_file = os.path.join(dest_dir, f"{os.path.splitext(map_filename)[0]}.png")
    gen_vis(parsed_map, annot_map, img_file)
