import os
import glob
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", help="filename")
args = vars(ap.parse_args())

if args['filename'] is not None:
    filenames = glob.glob(args['filename'])
else:
    filenames = glob.glob("*")

filenames.sort(key=lambda x: os.stat(x).st_mtime, reverse=False)

i = 1
for filename in filenames:
    os.rename(filename, str(i) + " - " + filename)
    i = i + 1