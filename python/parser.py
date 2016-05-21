#!/Users/roeeaharoni/anaconda/bin/python

#this python script parses the given files using the berkeley parser
import os
import sys

NUM_THREADS = 1
#INPUT_DIR = '/Users/roeeaharoni/Dropbox/master/thesis/mt_corpora/wmt13-data/plain/system-outputs/newstest2013/fr-en/'
#INPUT_DIR = '/Users/roeeaharoni/research_data/newstest_2010_2011_wmt12/'
#INPUT_DIR = '/Users/roeeaharoni/Dropbox/master/thesis/mt_corpora/itranslate4eu/'
INPUT_DIR = '/Users/roeeaharoni/research_data/icri-speech/ICSI-transcripts/txts/Bed015/'
OUTPUT_DIR = '/Users/roeeaharoni/research_data/icri-speech/ICSI-transcripts/txts/Bed015/parsed/'
#OUTPUT_DIR = '/Users/roeeaharoni/research_data/newstest_2010_2011_wmt12/to_parse/'
#OUTPUT_DIR = '/Users/roeeaharoni/research_data/wmt13-data/plain/system-outputs/newstest2013/fr-en/sentence_chunks/parsed/'
BERKELEY_DIR = '/Users/roeeaharoni/Dropbox/master/thesis/code/berkeley_parser/'

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def main(args):
    #split_results('/Users/roeeaharoni/research_data/sentence_chunks/48914_exp/sentence_chunks/parsed/lgt.ts.txt.tmp', OUTPUT_DIR)
    #return
    
    files = os.listdir(INPUT_DIR)
    for file in files:
        print files
        #if not (file.endswith('.DS_Store') or file.endswith('BLEU')) and file.endswith('newstest_2010_2011_wmt12.txt.tok.true.en'):
        if file.endswith('.txt'):
            print 'now parsing ' + file
            ensure_dir(OUTPUT_DIR + file)
            results_file = parse_file(INPUT_DIR + file, OUTPUT_DIR + file + '.tmp')
            split_results(results_file, OUTPUT_DIR + file)
    return
    
def parse_file(input_file, output_file):
    print 'starting to parse:'
    
    # tokenize first
    tokenize = True
    if tokenize:
        tokenized_file = input_file + '.tok'
        tokenizer_command_format = '~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < {0} > {1}'
        os.system(tokenizer_command_format.format(input_file, tokenized_file))
    
    # parse
    parser_command_format = 'java -jar berkeleyParser.jar -gr eng_sm6.gr -tokenize -inputFile {0} -outputFile {1} -nThreads {2}'
    os.chdir(BERKELEY_DIR)
    if tokenize:
        os.system(parser_command_format.format(tokenized_file, output_file, NUM_THREADS))
        os.system('rm {0}'.format(tokenized_file))
    else:
        os.system(parser_command_format.format(input_file, output_file, NUM_THREADS))
        
    print 'finished parsing!'
    return output_file

def split_results(output_file, output_dir):
    print 'splitting results to files:'
    ensure_dir(output_dir + '/')
    parsed_file = file(output_file, "rb").read()
    lines = parsed_file.split("\n")
    line_count = 0
    for line in lines:
        output = file(output_dir + '/' + str(line_count) + '.txt', "wb")
        output.write(lines[line_count])
        output.close()
        line_count += 1
    print 'DONE!'
    
if __name__ == "__main__":
    main(sys.argv)