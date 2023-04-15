map_id=$1
player1=$2
player2=$3
match_dir=${4:-"Match/"}

python3 playgame_mac.py --map "Maps/"$map_id --player1 "Players/"$player1 --player2 "Players/"$player2 --output $match_dir
