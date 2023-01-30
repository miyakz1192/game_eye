#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
import glob 
from collections import defaultdict

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
		self.code_label = defaultdict(int) #ResNet's label(str) and code(int) hash
		self.image_file = image_file
		self.get_resnet_labels()

	def run(self):
		print("===== RUN Game EYE =====")
		self.call_ssd()
		self.call_resnet()

	def get_resnet_labels(self):
		print("************* NEED TO MAKE LABEL and LABLE CODE HASH****")
		cmd = ["./run_resnet_labels.sh", self.RESNET_HOME]
		res = subprocess.check_output(cmd).decode('utf-8').strip().split("\n")
		res = res[3:] # skip header
		for i in res:
			file_name, code = i.split(" ") 
			file_name = os.path.basename(file_name)
			label , ext = os.path.splitext(file_name)
			self.code_label[int(code)] = label

	def call_ssd(self):
		cmd = ["./run_ssd.sh", self.SSD_HOME , self.GAME_EYE_HOME + self.image_file]
		res = subprocess.check_output(cmd).decode('utf-8').strip().split("\n")
		print("DEBUG: %s" % (res))
		log_dir = res[len(res)-1].split("IMAGE_LOG=")[1]
		print("DEBUG: log_dir = %s" % (log_dir))
		self.ssd_image_log_dir = log_dir

	def call_resnet(self):
		dres = DetectionResultContainer()
		dres.load(self.SSD_HOME + self.ssd_image_log_dir + "/result_data.pickle")
#		l = glob.glob(self.SSD_HOME + self.ssd_image_log_dir + "/*.jpg")
		max_label = None
		max_score = 0.0
		for i in dres.res:
			target = self.SSD_HOME + i.file_name
			cmd = ["./run_resnet.sh", self.RESNET_HOME , target]
			res = subprocess.check_output(cmd).decode('utf-8').strip().split("\n")
			res = res[len(res)-1]
			res = res.strip("()")
			code , score = res.split(",")
			code = int(code)
			score = float(score)
			label  = self.code_label[code]
			print("RESNET=%s, %f" % (label, score))
			if score > max_score:
				max_score = score
				max_label = label

		if max_label is not None:
			print("EYE_RESULT=%s, %f" % (max_label, max_score))

if __name__ == "__main__":
	eye = GameEye(args.image_file)
	eye.run()
