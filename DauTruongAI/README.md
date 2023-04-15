# Đấu Trường AI - Semifinal and Final Game
[Luật chơi](https://fb.watch/jI1MEVLyaf/)

Có thể sử dụng file `TeamRenamed.exe` để làm AI baseline chỉ nhằm mục đích phát triển AI bot của team bạn.
**Renamed** hy vọng AI của các năm sau sẽ đều mạnh hơn AI hiện tại của team.

Xem AI TeamRenamed thi đấu: [tại đây](https://www.facebook.com/100007708905334/videos/946877976733960/)

## How to run checker

Based on [this repo](https://github.com/vltanh/botwar-battleship)

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
cd DauTruongAI/back-office
python3 visualizer.py -r . -i path/to/TeamRenamed_TeamJazzy.json -t match
```
Result in [visualization](/DauTruongAI/back-office/visualization/) (file `.gif`)

### Benchmark

### Map generation