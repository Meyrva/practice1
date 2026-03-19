import os
import shutil

source = 'sample.txt'
copin = 'cops.txt'
shutil.copy(source, copin)

os.remove("del.txt")