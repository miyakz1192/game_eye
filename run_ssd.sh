#!/bin/bash
cd "$1" ; ./bin/edged.py $2 ; python3 predict.py weights/best_weight.pth ./edged.jpg "$2" ; cp result.jpg ~/game_eye
