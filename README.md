# Snake
Project for CIS 667 AI

Author: Junhao Chen, Dan li

Created by python 3.7 with pygame, numpy 

### Models 
Tree Searching: ExpectiMax

Machine Learning: Q learning

### Files
Using pygame to create a game GUI programming in game.py

ExpectiMax model setting up in expectiMax.py

Q Learning setting up in qlearning.py

### Run
Running the game python game.py default as a manul game, you can play it by keyboard

There are a lot of flag to modify the app

-a it is runing a game using A* 

-q it is runing a game using Q learning

-e it is running a game using ExpectiMax

-r it is running randomly, using it as benchmark

-p it will print more info when running

-i change a iterator-size

-vs change vision size which using in Qlearning and ExpectiMax

-f Load Qtable from the file, you can pass you file to it

### Examples 
Run q learing 500 time with the game to learn a Qtable

python game.py -q -i 500 

Run q learning with a specific file

python game.py -q -i 500 -f filename

Play the game with ExpectiMax 100 times

python game.py -e -i 100

Play the game with ExpectiMax and Q learning 100 times
python game.py -eq -i 100


