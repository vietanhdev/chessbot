import gc, os, sys, glob, argparse
import neural_chessboard.utils as utils
print("<<< \x1b[5;32;40m neural-chessboard \x1b[0m >>>")


from neural_chessboard.config import *
from neural_chessboard.utils import ImageObject
from neural_chessboard.slid import pSLID, SLID, slid_tendency #== step 1
from neural_chessboard.laps import LAPS                       #== step 2
from neural_chessboard.llr import LLR, llr_pad                #== step 3

from keras import backend as K
import cv2
load = cv2.imread
save = cv2.imwrite

#NC_SCORE = -1

################################################################################

def layer():
	global NC_LAYER, NC_IMAGE #, NC_SCORE
	
	print(utils.ribb("==", sep="="))
	print(utils.ribb("[%d] LAYER " % NC_LAYER, sep="="))
	print(utils.ribb("==", sep="="), "\n")

	# --- 1 step --- find all possible lines (that makes sense) ----------------
	print(utils.ribb(utils.head("SLID"), utils.clock(), "--- 1 step "))
	segments = pSLID(NC_IMAGE['main'])
	raw_lines = SLID(NC_IMAGE['main'], segments)
	lines = slid_tendency(raw_lines)

	# --- 2 step --- find interesting intersections (potentially a mesh grid) --
	print(utils.ribb(utils.head("LAPS"), utils.clock(), "--- 2 step "))
	points = LAPS(NC_IMAGE['main'], lines)
	#print(abs(49 - len(points)), NC_SCORE)
	#if NC_SCORE != -1 and abs(49 - len(points)) > NC_SCORE * 4: return
	#NC_SCORE = abs(49 - len(points))

	# --- 3 step --- last layer reproduction (for chessboard corners) ----------
	print(utils.ribb(utils.head(" LLR"), utils.clock(), "--- 3 step "))
	inner_points = LLR(NC_IMAGE['main'], points, lines)
	four_points = llr_pad(inner_points, NC_IMAGE['main']) # padcrop

	# --- 4 step --- preparation for next layer (deep analysis) ----------------
	print(utils.ribb(utils.head("   *"), utils.clock(), "--- 4 step "))
	print(four_points)
	try: NC_IMAGE.crop(four_points)
	except:
		utils.warn("unfortunately, but the next layer is not needed")
		NC_IMAGE.crop(inner_points)

	print("\n")

################################################################################

def detect(img):
	utils.reset()
	global NC_LAYER, NC_IMAGE, NC_CONFIG

	NC_IMAGE = ImageObject(img)
	NC_LAYER = 0

	for _ in range(NC_CONFIG['layers']):
		NC_LAYER += 1; layer()

	print("Detect board done!")

	K.clear_session(); gc.collect() # FIX: tensorflow#3388
	return NC_IMAGE['orig']
	
################################################################################

