import os
import logging
from os.path import splitext
from collections import Counter
path=os.getcwd().split(os.sep)[-1]
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)
logging.debug('Start of script')

def compare_text_flac_mp3(path):
    #List containing all file names + their extension in path directory
    myDir = os.listdir(path)
    #logging.debug('The list of folders is' + str(myDir))
    #List containing all file names without their extension
    l = [splitext(filename)[0] for filename in myDir]

    #Count occurrences
    a = dict(Counter(l))
    #Loop files name that have same name and different extension
    for k,v in a.items():
        if v >= 2:
            if os.path.exists(path + '/' + k + '.mp3'):
                logging.debug('Deleting file ' + path + '/' + k + '.mp3')
                os.remove(path + '/' + k + '.mp3')
        else:
            print ('nothing to delete')

compare_text_flac_mp3(path)
logging.debug('End of script')