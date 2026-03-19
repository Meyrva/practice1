import os
import shutil

files = os.listdir('new_directory')

for f in files:
    if f.endswith('.txt'):
        print("txt files:", f)
# Move/copy files between directories


shutil.copy2("file.txt","new_directory")