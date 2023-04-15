@ECHO OFF
SET MAP_ID=%1
SET PLAYER1=%2
SET PLAYER2=%3
if "%4"=="" (
    SET MATCH_DIR=Match/
) else (
    SET MATCH_DIR=%1
)
python playgame.py --map Maps/%MAP_ID% --player1 Players/%PLAYER1% --player2 Players/%PLAYER2% --output %MATCH_DIR% 
