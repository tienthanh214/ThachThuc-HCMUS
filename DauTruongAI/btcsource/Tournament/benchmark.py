'''
Benchmarking script for DauTruongAI, export result to csv file
Statistic match result of 2 teams
Author: minhkhoi1026
'''

import itertools
import json
import os
import shutil
import subprocess
import concurrent.futures
import sys
import pandas as pd
from tqdm import tqdm

# mode =  sys.args[1]  # "windows" || "linux"
# team1 = sys.args[2]
# team2 = sys.args[3]
# NUM_TRY = sys.args[4]
team1 = "TeamThanh"
team2 = "TeamTrucJ"
NUM_TRY = 5
mode = "linux"  # "windows" || "linux"
map_dir = "Maps"
result_dir = "Stats"
run_file = "run.sh" if mode == "linux" else "run.bat"
K_list = [10, 20] # , 30, 40, 50, 60, 70, 80, 90, 100


def clean_dirs():
    for i in range(NUM_TRY):
        match_dir = f"Match{i}/"
        if os.path.exists(match_dir):
            shutil.rmtree(match_dir)

        player1_dir = f"Players/{team1}{i}"
        if os.path.exists(player1_dir):
            shutil.rmtree(player1_dir)

        player2_dir = f"Players/{team2}{i}"
        if os.path.exists(player2_dir):
            shutil.rmtree(player2_dir)


def create_player_clone(base_player_dir, team, i):
    # create player dir
    src_player_dir = os.path.join(base_player_dir, f"{team}")
    dst_player_dir = os.path.join(base_player_dir, f"{team}{i}")
    shutil.copytree(src_player_dir, dst_player_dir)

    # renamed execute file
    old_player_file = os.path.join(
        dst_player_dir, f"{team}{'.exe' if mode == 'windows' else ''}"
    )
    new_player_file = os.path.join(
        dst_player_dir, f"{team}{i}{'.exe' if mode == 'windows' else ''}"
    )
    os.rename(old_player_file, new_player_file)


def init_dirs():
    os.makedirs(result_dir, exist_ok=True)
    base_player_dir = "Players"
    for i in range(NUM_TRY):
        # create match dir
        match_dir = f"Match{i}"
        os.makedirs(match_dir, exist_ok=True)

        # create player2 clone dir
        create_player_clone(base_player_dir, team1, i)
        create_player_clone(base_player_dir, team2, i)


def change_k_of_map(map_filepath, K):
    # Open the file in read mode
    with open(map_filepath, "r") as f:
        # Read the file contents
        lines = f.readlines()

        # Get the first line and split it by space
        first_line_entries = lines[0].split()

        # Modify the third entry
        first_line_entries[2] = str(K)

        # Replace the first line in the original list with the modified list
        lines[0] = " ".join(first_line_entries) + "\n"

    # Write the modified contents back to the file
    with open(map_filepath, "w") as f:
        f.writelines(lines)


# Define a function to execute a shell script
def execute_script(map, team1, team2, i, K):
    match_dir = f"Match{i}"

    if mode == "linux":
        command = f"sh ./{run_file} {map} {team1}{i} {team2}{i} {match_dir}"
    else:
        command = f".\\{run_file} {map} {team1}{i} {team2}{i} {match_dir}"
    command = command.split()
    _ = subprocess.run(command, capture_output=True)

    with open(
        os.path.join(
            match_dir, f"{team1}{i}_{team2}{i}_{os.path.splitext(map)[0]}.json"
        ),
        "r",
    ) as f:
        match_info = list(json.load(f).items())
        match_info.sort(key=lambda x: int(x[0]))
        result = match_info[-1]

    return {
        "map": map,
        "team1": team1,
        "team2": team2,
        "result": result,
        "i": i,
        "K": K,
    }


def benchmark():
    data = list()
    map_list = list(os.listdir(map_dir))

    for K, map in tqdm(
        itertools.product(K_list, map_list), total=len(K_list) * len(map_list)
    ):
        change_k_of_map(os.path.join(map_dir, map), K)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list()
            for i in range(NUM_TRY):
                results.append(executor.submit(execute_script, map, team1, team2, i, K))

            for future in concurrent.futures.as_completed(results):
                data.append(future.result())
    return data


def save_result(data):
    rows = list()
    columns = [
        "map_id",
        "K",
        "ith_try",
        "last_step",
        "name1",
        "point1",
        "shield1",
        "alive1",
        "name2",
        "point2",
        "shield2",
        "alive2",
    ]
    for raw_row in data:
        map_id = raw_row["map"]
        K = raw_row["K"]
        ith_try = raw_row["i"]
        last_step = raw_row["result"][0]
        name1 = raw_row["team1"]
        point1 = raw_row["result"][1]["point1"]
        shield1 = raw_row["result"][1]["shield1"]
        alive1 = raw_row["result"][1]["alive1"]
        name2 = raw_row["team2"]
        point2 = raw_row["result"][1]["point2"]
        shield2 = raw_row["result"][1]["shield2"]
        alive2 = raw_row["result"][1]["alive2"]

        rows.append(
            [
                map_id,
                K,
                ith_try,
                last_step,
                name1,
                point1,
                shield1,
                alive1,
                name2,
                point2,
                shield2,
                alive2,
            ]
        )

    rows.sort(key=lambda x: (x[0], x[1], x[2]))

    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(os.path.join(result_dir, f"{team1}_{team2}_stat.csv"), index=None)


clean_dirs()
init_dirs()
data = benchmark()
save_result(data)
clean_dirs()
