import os
import shutil

# Move a file by renaming it's path
os.rename('/Users/billy/d1/xfile.txt', '/Users/billy/d2/xfile.txt')

# Move a file from the directory d1 to d2
shutil.move('/Users/billy/d1/xfile.txt', '/Users/billy/d2/xfile.txt')