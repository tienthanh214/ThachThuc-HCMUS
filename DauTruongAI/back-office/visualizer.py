import argparse
from PIL import Image
import glob
import imageio
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import copy
import numpy as np

sns.set(rc={"figure.figsize": (11.7, 8.27)})
color_map = [[0.2,0.2,0.2,1.],
            [0.980, 0.341, 0.147,1.],
            [0.890, 0.890, 0.890,1.],
            [0.147, 0.522, 0.980,1.],
            [0.147, 0.522, 0.980,1.],
            [0.147, 0.522, 0.980,1.],
            [0.147, 0.522, 0.980,1.],
            [1.00, 0.984, 0.0500,1.]]


def get_symmetric_count(map, M, N):
    x = [0, 0, 0, 0]
    for i in range(M):
        for j in range(N):
            if map[i][j] == map[j][i]:
                x[0] += 1
            elif map[i][j] == map[M - i - 1][N - j - 1]:
                x[1] += 1
            elif map[i][j] == map[M - i - 1][j]:
                x[2] += 1
            elif map[i][j] == map[i][N - j - 1]:
                x[3] += 1
    return x


def get_wrong_cell_symmetric(map, M, N, sym_type):
    res = list()
    for i in range(M):
        for j in range(N):
            if sym_type == 0 and map[i][j] != map[j][i]:
                res.append((i + 1, j + 1))
            elif sym_type == 1 and map[i][j] == map[M - i - 1][N - j - 1]:
                res.append((i + 1, j + 1))
            elif sym_type == 2 and map[i][j] == map[M - i - 1][j]:
                res.append((i + 1, j + 1))
            elif sym_type == 3 and map[i][j] == map[i][N - j - 1]:
                res.append((i + 1, j + 1))
    return res


def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]


def gen_vis(map, annot, title=None, save_path=None):
    # create a heatmap of the data
    plt.clf()
    sns.heatmap(
        map,
        vmin=-5,
        vmax=9,
        annot=annot,
        annot_kws={"size": 16},
        fmt="s",
        cmap=color_map
    )
    if title:
        plt.title(title, fontsize=26)

    if save_path:
        plt.savefig(save_path)


def parse_map(lines, delim=" "):
    parsed_map = lines
    for i, _ in enumerate(parsed_map):
        parsed_map[i] = parsed_map[i].strip().split(delim)

    raw_map = copy.deepcopy(parsed_map)
    sum = 0
    M = len(parsed_map)
    N = len(parsed_map[0])
    for i in range(M):
        for j in range(N):
            if parsed_map[i][j].isdigit():
                parsed_map[i][j] = int(parsed_map[i][j])
                sum += parsed_map[i][j]
            elif parsed_map[i][j] == "D":
                parsed_map[i][j] = -10
            elif parsed_map[i][j] == "S":
                parsed_map[i][j] = 10
    return parsed_map, raw_map, sum


def gen_visualizer_maps(root, src_dir, dest_dir):
    src_dir = os.path.join(root, src_dir)
    dest_dir = os.path.join(root, dest_dir)
    os.makedirs(dest_dir, exist_ok=True)

    for map_filename in tqdm(os.listdir(src_dir)):
        lines = None

        with open(os.path.join(src_dir, map_filename), "r") as f:
            lines = f.readlines()

        M, N, K = list(map(int, lines[0].split(" ")))

        parsed_map, annot_map, sum = parse_map(lines[1:])

        # check if sum of values in map equal 100
        if sum != 100:
            print(
                f"[{map_filename}]: value sum does not equal 100. Calculated value {sum}!"
            )

        # check if center cell value are 0
        if parsed_map[M // 2][N // 2] != 0:
            print(
                f"[{map_filename}]: Exected 0 at cell ({M // 2 + 1}, {N // 2 + 1}). Got {annot_map[M // 2][N // 2]}!"
            )

        # check if map are symmetric
        try:
            sym_count = get_symmetric_count(parsed_map, M, N)
            sym_count.index(M * N)
        except ValueError:
            sym_type = argmax(sym_count)
            wrong_cells = get_wrong_cell_symmetric(parsed_map, M, N, sym_type)
            sym_str_list = ["Main diagonal", "Anti diagonal", "Horizontal", "Vertical"]
            print(
                f"[{map_filename}]: Does not symmetric! Symmetric type: {sym_str_list[sym_type]}. "
                f"Founded wrong cells: {wrong_cells}"
            )

        img_file = os.path.join(dest_dir, f"{os.path.splitext(map_filename)[0]}.png")
        gen_vis(parsed_map, annot_map, save_path=img_file)


def gen_gif(input_dir, output_filepath):
    # Get a list of all image files in the input directory
    images = glob.glob(f"{input_dir}/*.png")
    images.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    with imageio.get_writer(output_filepath, mode="I", duration=0.5) as writer:
        for filename in images:
            # Open the image file using PIL
            image = np.array(Image.open(filename))

            # Add the image to the writer
            writer.append_data(image)


def gen_visualizer_match(root, match_filepath, dest_dir):
    dest_dir = os.path.join(root, dest_dir)
    for file in os.listdir(dest_dir):
        if file.split(".")[1] == "png":
            os.remove(os.path.join(dest_dir,file))
    match_filepath = os.path.join(root, match_filepath)

    team_name1, team_name2, map_id = os.path.basename(match_filepath).split("_")[0:3]

    os.makedirs(dest_dir, exist_ok=True)

    with open(match_filepath, "r") as f:
        match_info = list(json.load(f).items())
    match_info.sort(key=lambda x: int(x[0]))

    for key, step_info in tqdm(match_info):
        lines = step_info["map_humanreadable"]
        parsed_map, annot_map, sum = parse_map(lines, delim=",")

        x1, y1 = step_info["x1"] - 1, step_info["y1"] - 1
        annot_map[x1][y1] = "UwU"
        parsed_map[x1][y1] = 100 if step_info["shield1"] else -2

        x2, y2 = step_info["x2"] - 1, step_info["y2"] - 1
        annot_map[x2][y2] = "^.^"
        parsed_map[x2][y2] = 100 if step_info["shield2"] else -2

        img_file = os.path.join(dest_dir, f"{os.path.splitext(key)[0]}.png")
        title = f'Step remain: {step_info["moveleft"]}, {team_name1} UwU: {step_info["point1"]}, {team_name2} ^.^: {step_info["point2"]}'
        gen_vis(parsed_map, annot_map, title=title, save_path=img_file)
    gen_gif(dest_dir, os.path.join(dest_dir, f"{team_name1}_{team_name2}_{map_id}.gif"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Dau truong AI visualizer",
        description="Generate a visualizer of map and match",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["map", "match"],
        required=True,
        help="type of visualize you want to generate"
        "'map' for maps visualization and 'match' for match visualization",
    )
    parser.add_argument(
        "-r",
        "--root",
        default=".",
        help="root directory where contains data to visualize",
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="path of source directory containes maps (in text format)"
        " or path of match file (in json format)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="visualization",
        help="path to result directory where you want to save result",
    )
    args = parser.parse_args()
    if args.type == "map":
        gen_visualizer_maps(args.root, args.input, args.output)
    elif args.type == "match":
        gen_visualizer_match(args.root, args.input, args.output)
