#!/usr/bin/python

import os
from PIL import Image
import uuid
import shutil

import sys


WIDTH=36
HEIGHT=18
COUNTRY='us'

#WIDTH=52
#HEIGHT=13
#COUNTRY='eu'

#constants
OPENCV_DIR= '/home/mhill/projects/alpr/libraries/opencv/bin'
SAMPLE_CREATOR = OPENCV_DIR + '/opencv_createsamples'

BASE_DIR            = '/home/mhill/projects/alpr/samples/training/'

OUTPUT_DIR          = BASE_DIR + "out/"
INPUT_NEGATIVE_DIR  = BASE_DIR + 'raw-neg/'
INPUT_POSITIVE_DIR  = BASE_DIR + COUNTRY + '/'
OUTPUT_NEGATIVE_DIR  = BASE_DIR + 'negative/'
OUTPUT_POSITIVE_DIR  = BASE_DIR + 'positive/'


POSITIVE_INFO_FILE  = OUTPUT_POSITIVE_DIR + 'positive.txt'
NEGATIVE_INFO_FILE  = OUTPUT_NEGATIVE_DIR + 'negative.txt'
VEC_FILE            = OUTPUT_POSITIVE_DIR + 'vecfile.vec'



vector_arg = '-vec %s' % (VEC_FILE)
width_height_arg = '-w %d -h %d' % (WIDTH, HEIGHT)


def print_usage():
    print "Usage: prep.py [Operation]"
    print "   -- Operations --"
    print "  neg        -- Prepares the negative samples list"
    print "  pos        -- Copies all the raw positive files to a opencv vector"
    print "  showpos    -- Shows the positive samples that were created"
    print "  train      -- Outputs the command for the Cascade Training algorithm"

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1



command=""

if command != "":
    pass
elif len(sys.argv) != 2:
    print_usage()
    exit()
else:
    command = sys.argv[1]


if command == "neg":
    print "Neg"

    # Get rid of any spaces
    for neg_file in os.listdir(INPUT_NEGATIVE_DIR):
        if " " in neg_file:
            fileName, fileExtension = os.path.splitext(neg_file)

            newfilename =  str(uuid.uuid4()) + fileExtension
            #print "renaming: " + files + " to "+ root_dir + "/" + str(uuid.uuid4()) + fileExtension
            os.rename(INPUT_NEGATIVE_DIR + neg_file, INPUT_POSITIVE_DIR + newfilename)


    f = open(NEGATIVE_INFO_FILE,'w')
    ## Write a list of all the negative files
    for neg_file in os.listdir(INPUT_NEGATIVE_DIR):
        if os.path.isdir(INPUT_NEGATIVE_DIR + neg_file):
            continue

        shutil.copy2(INPUT_NEGATIVE_DIR + neg_file, OUTPUT_NEGATIVE_DIR + neg_file )

        f.write(neg_file + "\n")


    f.close()

elif command == "pos":
    print "Pos"
    info_arg = '-info %s' % (POSITIVE_INFO_FILE)

    # Copy all files in the raw directory and build an info file

    ## Remove all files in the output positive directory
    for old_file in os.listdir(OUTPUT_POSITIVE_DIR):
        os.unlink(OUTPUT_POSITIVE_DIR + old_file)

    ## First, prep the sample filenames (make sure they have no spaces)
    for files in os.listdir(INPUT_POSITIVE_DIR):
        if os.path.isdir(INPUT_POSITIVE_DIR + files):
            continue

        # Rename the file if it has a space in it
        newfilename = files
        if " " in files:
            fileName, fileExtension = os.path.splitext(files)

            newfilename =  str(uuid.uuid4()) + fileExtension
            #print "renaming: " + files + " to "+ root_dir + "/" + str(uuid.uuid4()) + fileExtension
            os.rename(INPUT_POSITIVE_DIR + files, INPUT_POSITIVE_DIR + newfilename)

        # Copy from the raw directory to the positive directory
        shutil.copy2(INPUT_POSITIVE_DIR + newfilename, OUTPUT_POSITIVE_DIR + newfilename )


    total_pics = 0
    ## Create the positive.txt input file
    f = open(POSITIVE_INFO_FILE,'w')
    for filename in os.listdir(OUTPUT_POSITIVE_DIR):
        if os.path.isdir(OUTPUT_POSITIVE_DIR + filename):
            continue

        if filename.endswith(".txt"):
            continue
	try:
		img = Image.open(OUTPUT_POSITIVE_DIR + filename)

		# get the image's width and height in pixels
		width, height = img.size
		f.write(filename + " 1 0 0 " + str(width) + " " + str(height) + '\n')

		total_pics = total_pics + 1
	except IOError:
		print "Exception reading image file: " + filename

    f.close()




    # Collapse the samples into a vector file
    execStr = '%s/opencv_createsamples %s %s %s -num %d' % (OPENCV_DIR, vector_arg, width_height_arg, info_arg, total_pics )
    print execStr

    os.system(execStr)
    #opencv_createsamples -info ./positive.txt -vec ../positive/vecfile.vec -w 120 -h 60 -bg ../negative/PentagonCityParkingGarage21.jpg -num 100


elif command == "showpos":
    print "SHOW"
    execStr = '%s/opencv_createsamples -vec %s -w %d -h %d' % (OPENCV_DIR, VEC_FILE, WIDTH, HEIGHT )
    print execStr
    os.system(execStr)
    #opencv_createsamples -vec ../positive/vecfile.vec -w 120 -h 60
elif command == "train":
    print "TRAIN"

    data_arg = '-data %s/' % (OUTPUT_DIR)
    bg_arg = '-bg %s' % (NEGATIVE_INFO_FILE)

    try:
	num_pos_samples = file_len(POSITIVE_INFO_FILE)
    except:
	num_pos_samples = -1
    num_neg_samples = file_len(NEGATIVE_INFO_FILE)

    execStr = '%s/opencv_traincascade %s %s %s %s -numPos %d -numNeg %d -maxFalseAlarmRate 0.45 -featureType LBP -numStages 13' % (OPENCV_DIR, data_arg, vector_arg, bg_arg, width_height_arg, num_pos_samples, num_neg_samples )

    print "Execute the following command to start training:"
    print execStr
    #opencv_traincascade -data ./out/ -vec ./positive/vecfile.vec -bg ./negative/negative.txt -w 120 -h 60 -numPos 99 -numNeg 5  -featureType LBP -numStages 8
    #opencv_traincascade -data ./out/ -vec ./positive/vecfile.vec -bg ./negative/negative.txt -w 120 -h 60 -numPos 99 -numNeg 5  -featureType LBP -numStages 20
elif command == "SDFLSDFSDFSDF":

    root_dir = '/home/mhill/projects/anpr/AlprPlus/samples/svm/raw-pos'
    outputfilename = "positive.txt"



else:
    print_usage()
    exit()
