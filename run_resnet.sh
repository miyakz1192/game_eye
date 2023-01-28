#!/bin/bash
cd "$1" ; python3 /home/a/pytorch_ssd/bin/edged.py $2 ; python3 core/resnet34.py single ./edged.jpg "$2"
