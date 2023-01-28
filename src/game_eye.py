#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from detection_result import *

parser = argparse.ArgumentParser()
parser.add_argument("image_file", type=str)
args = parser.parse_args()

class GameEye:
	SSD_HOME             = "/home/a/pytorch_ssd/"
	RESNET_HOME          = "/home/a/resset/"
	GAME_EYE_HOME        = "/home/a/game_eye/"
	RESULT_JPG_FILE_PATH = "./result/result.jpg"
	PICKLE_FILE_PATH     = SSD_HOME + "/result_data.pickle"

	def __init__(self, image_file):
		self.image_file = image_file

	def run(self):
		print("===== RUN Game EYE =====")
		self.call_ssd()

	def call_ssd(self):
		cmd = ["./run_ssd.sh", self.SSD_HOME , self.GAME_EYE_HOME + self.image_file]
		res = subprocess.check_output(cmd).decode('utf-8').strip().split("\n")
		print("DEBUG: %s" % (res))
		log_dir = res[len(res)-1].split("IMAGE_LOG=")[1]
		print("DEBUG: log_dir = %s" % (log_dir))
		return log_dir

	def call_resnet(self):
		pass


if __name__ == "__main__":
	eye = GameEye(args.image_file)
	eye.run()
