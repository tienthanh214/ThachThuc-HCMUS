# Đấu Trường AI - Semifinal and Final Game
[Luật chơi](https://fb.watch/jI1MEVLyaf/)

Có thể sử dụng file `TeamRenamed.exe` để làm AI baseline chỉ nhằm mục đích phát triển AI bot của team bạn.
**Renamed** hy vọng AI của các năm sau sẽ đều mạnh hơn AI hiện tại của team.

Xem AI TeamRenamed thi đấu: [tại đây](https://www.facebook.com/100007708905334/videos/946877976733960/)

## Baseline template
This code template [here](/DauTruongAI/dev/main.cpp) provides the basic structure for creating an AI agent that can play a game on a given map. It includes:
- A set of constant definitions and a `MapInfo` struct that stores information about the map, such as its dimensions, the location of shields and dangerous zones, and the symmetry type of the map. 
- A `BaseSolution` class that can be extended to implement different AI strategies for playing the game.

The code includes functions for checking whether a given coordinate is inside the map, checking the symmetry of the map, and printing debug information. It also includes a random number generator for use in some AI algorithms.

The main function currently returns 0 and needs to be modified to call the run function of an AI agent that implements the `BaseSolution` class.

After all, you can create an executable of your agent using the `make` command:
```bash
make FNAME=<your-file.cpp>
```

## How to run checker

Based on the official source of Thach Thuc organizer.

The folder **must** be arranged this specific way:

```
	<root>
	|- checker.exe
	|- Maps
		|- <map_id>.txt
		|- ...
	|- Players
		|- <team_id> (always start with "Team", i.e "Team*")
			|- <team_id>.exe
		|- ...
	|- Match
```

With:
- `Maps` folder: contains map with following format (see example in [Map.txt](/DauTruongAI/btcsource/Tournament/Maps/Map.txt))
```txt
	m n k
	<map data of m lines, each containing n strings seperated by space>
```
- `Players` folder: contains players executable
- `Match` folder: Result of a match in ```<team_id>_<team_id>_<map_id>.txt```.

To run on **Windows** (exe file): cd to `btcsource/Tournament`
```cmd
run.bat Map.txt TeamRenamed TeamYou
```

To run on **Linux/MacOS** (binary file):
```bash
sh run.sh Map.txt TeamRenamed TeamYou
```

## Supportive Tools
### Visualization
Simple visualize match result
```bash
scd DauTruongAI/back-office
python3 visualizer.py -r . -i <path/to/match_file.json> -t match
```
example:
```bash
python3 visualizer.py -r . -i ../btcsource/Tournament/Match/TeamTruc_TeamKhoi_Map.json -t match     
```
Result in [visualization](/DauTruongAI/back-office/visualization/) (file `.gif`)

### Benchmark
This is a benchmarking script that allows you to compare the performance of two AI agents in a game. The script exports the result to a csv file and provides statistics on the match results of the two teams.

### Map generation
cd DauTruongAI/back-office
python3 gen_map.py -n <num_of_maps> -o <path_to_save_maps>
