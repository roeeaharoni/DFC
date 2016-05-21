#!/Users/roeeaharoni/anaconda/bin/python

# run the stanford corenlp tagger on the files in the folders in INPUT_DIR
import os
import sys

INPUT_DIR = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks'
CORE_NLP_DIR = '/Users/roeeaharoni/research_data/icri-speech/stanford-corenlp-full-2015-04-20'

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main(args):
    tag_directory(INPUT_DIR)
    return
    
    dirs = os.listdir(INPUT_DIR)
    print 'found:'
    print dirs
    for dir in dirs:
        tag_directory(INPUT_DIR + '/' + dir)
    
def tag_directory(dirname):
    files = os.listdir(dirname)
    print 'found:'
    print files
    print 'starting to tag:'
    tagger_command_format = 'java -cp stanford-corenlp-3.5.2-javadoc.jar:stanford-corenlp-3.5.2-models.jar:xom.jar:stanford.corenlp-3.5.2-sources.jar:stanford-corenlp-3.5.2.jar:joda-time.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos -file {0} -outputDirectory {1}'
    
    for file in files:
        #if not file.startswith('25k_25k'):
        #    continue
        
        output_dir = dirname + '/annotations/' + file + '/'
        ensure_dir(output_dir)
        os.chdir(CORE_NLP_DIR)
        os.system(tagger_command_format.format(dirname + '/' + file, output_dir))
        
        print 'tagged ' + file

if __name__ == "__main__":
    main(sys.argv)
    
"""an example console line for activating corenlp tagger on a directory of chopped txt files"""    
"""java -cp stanford-corenlp-1.3.5-javadoc.jar:stanford-corenlp-1.3.5-models.jar:xom.jar:stanford.corenlp-1.3.5-sources.jar:stanford-corenlp-1.3.5.jar:joda-time.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos -file ../google.txt -outputDirectory ../annotations/google"""
