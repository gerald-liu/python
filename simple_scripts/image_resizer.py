from PIL import Image
import os
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", help="filename")
ap.add_argument("-s", "--size", help="max file size in bytes")
args = vars(ap.parse_args())

if args['size'] is not None:
    max_size = args['size']
else:
    max_size = 1024 * 1024 * 5

try:
    name, ext = os.path.splitext(args['filename'])
    ratio = math.sqrt((max_size - 1) / os.path.getsize(args['filename']))
except Exception as e:
    print("Error in filename or max size.")
    quit()

try:
    img = Image.open(args['filename']).copy()
    size = tuple(x * ratio for x in img.size)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(name + "_small" + ext, quality=95)
except Exception as e:
    print("Error in compression.")