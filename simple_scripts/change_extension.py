# python script.py old_ext new_ext

import os
import sys

old_ext = '.' + sys.argv[1]
new_ext = '.' + sys.argv[2]

print(old_ext)
print(new_ext)

for file_basename in os.listdir():
    filename, ext = os.path.splitext(file_basename)
    print(ext)
    if ext == old_ext:
        os.rename(file_basename, filename + new_ext)
