import os
import sys

author_name = sys.argv[1]

def get_target_basename(filename, ext, author):
    return filename + '_' + author + ext

for file_basename in os.listdir():
    filename, ext = os.path.splitext(file_basename)
    os.rename(file_basename, get_target_basename(filename, ext, author_name))
