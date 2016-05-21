#!/Users/roeeaharoni/anaconda/bin/python

# run the WERater Intel tool to get WER results
import os
import sys

# INPUT_DIR = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged'
INPUT_DIR = '/Users/roeeaharoni/research_data/icri-speech/NAIST/txts/NAIST/fixed'
REF_PATH = INPUT_DIR + '/trans.txt'
WER_command_format = 'java -cp /Users/roeeaharoni/Dropbox/icri-ci-speech/code/java/WERaterWrapper/WERwrapper/bin/WERater_1.0.jar:/Users/roeeaharoni/Dropbox/icri-ci-speech/code/java/WERaterWrapper/WERwrapper/bin WERwrapper {0} {1} {2}'

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main(args):
    tag_directory(INPUT_DIR)
    return
    
def tag_directory(dirname):
    files = os.listdir(dirname)
    print 'found:'
    print files
    print 'starting to measure WER:'
    
    for file in files:
        output_file = INPUT_DIR + '/' + file + '_WER.txt'
        os.system(WER_command_format.format(REF_PATH, INPUT_DIR + '/' + file, output_file))
        print 'calculated WER for file  ' + file

if __name__ == "__main__":
    main(sys.argv)