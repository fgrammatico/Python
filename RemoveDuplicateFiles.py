import os
from os.path import splitext
from collections import Counter

def compare_text_flac_mp3(path):
    #List containing all file names + their extension in path directory
    myDir = os.listdir(path)
    #List containing all file names without their extension
    l = [splitext(filename)[0] for filename in myDir]

    #Count occurrences
    a = dict(Counter(l))
    #Loop files name that have same name and different extension
    for k,v in a.items():
        if v > 1:
            if os.path.exists('''/mnt/md-name-H4cKn3t:0/Music/Audio_Collection/Rock/'''+ k + '.mp3'):
                #If path exist then remove the duplicate file
                os.remove('''/mnt/md-name-H4cKn3t:0/Music/Audio_Collection/Rock/'''+ k + '.mp3')
            else:
                print ('nope')
compare_text_flac_mp3('/mnt/md-name-H4cKn3t:0/Music/Audio_Collection/Rock')
