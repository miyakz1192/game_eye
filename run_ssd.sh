#!/bin/bash
cd "$1" ; ./bin/edged.py $2 ; python3 predict.py weights/close_weight_1.2027226681531218.pth ./edged.jpg "$2"
