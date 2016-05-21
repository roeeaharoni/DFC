#!/Users/roeeaharoni/anaconda/bin/python

import csv
import os
from pyExcelerator import *
import sys
from xml.etree import ElementTree
import re


# root data directory
# ROOT_DATA_DIR = '/Users/roeeaharoni/research_data/icri-speech/ICSI-transcripts'
# ROOT_DATA_DIR = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Robocup_Rockin_merged'
ROOT_DATA_DIR = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/'
ROOT_OUTPUT_DIR = ROOT_DATA_DIR + '/sentence_chunks/'

def main():
    
    # go through every folder in the data 
    
    # parse the csv transcriptions files into txt files
    #parse_csv_to_txt()
    
    # create n-best lists for every conversation
    #parse_nbest_to_txt(5)
    
    # make sure that the n-best lists are in the same size as the transcripts and without missing values
    # ensure_extracted_data(ROOT_DATA_DIR, ROOT_OUTPUT_DIR)
    
    # merge all the n-best lists into large n-best lists
    #create_merged_n_best_corpora()
    
    # run WER for every (large) n-best list
    # done in WERwrapper.java
    
    # break the text into sentence chunks
    files = os.listdir(ROOT_DATA_DIR)
    # files = ['trans.txt']
    for file in files:
        if(file == '.DS_Store'):
            continue
        ensure_dir(ROOT_OUTPUT_DIR + '/' + file)
        break_txt_to_sentence_chunks(ROOT_DATA_DIR + '/' + file, ROOT_OUTPUT_DIR + '/' + file)
    
    # run the classification experiment for every n-best list

    # parse the n best results from the .xml files into a .txt file
    #parse_nbest_to_txt(4)
    return

# this method creates corpora from all the files in the "fixed" directories created by the ensure_extracted_data() method.
def create_merged_n_best_corpora():
    conversation_dirs = os.listdir(ROOT_OUTPUT_DIR + '/txts/')
    
    # stores the accumulated data from all the n-best and transcription files in a dictionary
    file_name_2_lists = {}
    for dir in conversation_dirs:
        file_len = -1
        if(dir == '.DS_Store' or dir == 'bad'):
            continue
        fixed_files = os.listdir(ROOT_OUTPUT_DIR + '/txts/' + dir + '/txts/fixed/')
        
        # add the data from every file to the dictionary
        for file in fixed_files:
            if(file == '.DS_Store' or file == 'fixed'):
                continue
            f = open(ROOT_OUTPUT_DIR + '/txts/' + dir + '/txts/fixed/' + file)
            content = f.readlines()
            if(file_len == -1):
                file_len = len(content)
            else:
                if(len(content) != file_len):
                    print 'files are not in same length: ' + dir + '/' + file
                
            if(file in file_name_2_lists):
                file_name_2_lists[file] = file_name_2_lists[file] + content
            else:
                file_name_2_lists[file] = content
            f.close()
    ensure_dir(ROOT_OUTPUT_DIR + '/merged/txts/')
    for file in file_name_2_lists:
        f = open(ROOT_OUTPUT_DIR + '/merged/txts/' + file, 'w')
        
        # make sure all rows end with \n to avoid misalignment when joining
        for i,l in enumerate(file_name_2_lists[file]):
            if(not l.endswith('\n')):
                file_name_2_lists[file][i] = file_name_2_lists[file][i] + '\n'
                
        # write merged data to file
        f.write(''.join(file_name_2_lists[file]))
        f.close()
        print 'wrote merged ' + file
    return


# make sure the transcripts are aligned to the n-best files, removes empty lines and their counterpart
def ensure_extracted_data(input_dir, output_dir):
    # conversation_dirs = os.listdir(ROOT_OUTPUT_DIR + '/txts/')
    conversation_dirs = os.listdir(input_dir)
    for dir in conversation_dirs:
        if(dir == '.DS_Store' or dir == 'bad'):
            continue
        f_trans = open(input_dir + '/' + dir + '/trans.txt','r+')
        trans_lines = f_trans.readlines()
        f_trans.close()
        trans_empty_indexes = []
        
        # check which rows are empty in the transcripted data
        for i, j in enumerate(trans_lines):
            if(len(j.strip().replace('\n','')) == 0):
                trans_empty_indexes.append(i)

        if len(trans_empty_indexes) > 0:
            print 'found {} empty lines in {}'.format(len(trans_empty_indexes), f_trans)
        else:
            print 'no empty lines in {}'.format(f_trans)

        files = os.listdir(input_dir + '/' + dir)
        total_empty = []
        
        # find minimum max len
        min_max_len = 9999999999
        for file in files:
            if(file == '.DS_Store' or file == 'fixed'):
                continue
            f = open(input_dir + '/' + dir + '/' + file,'r+')
            lines = f.readlines()
            f.close()
            min_max_len = min(min_max_len, len(lines))
        
        # find all empty indexes in all files
        for file in files:
            if(file == '.DS_Store' or file == 'fixed'):
                continue
                
            f = open(input_dir + '/' + dir + '/' + file,'r+')
            lines = f.readlines()
            f.close()
            
            if(len(lines) != len (trans_lines)):
                print 'files are not in same length! lines len:' + str(len(lines)) + ' trans len: ' + str(len(trans_lines)) + ' file:' + dir + '/' + file
                continue
            
            # check which rows are empty in the n-best data
            empty_indexes = []
            for i, j in enumerate(lines):
                if(len(j.strip().replace('\n','')) == 0):
                    empty_indexes.append(i)
                    
            total_empty = list(set(total_empty + trans_empty_indexes + empty_indexes))
        
        # define which indexes to use (only ones which are never empty)
        final_indexes = range(min_max_len)
        for x in total_empty:
            if(x < min_max_len):
                final_indexes.remove(x)
        
        # remove empty rows on both files and re-write them fixed
        for file in files:
            if(file == '.DS_Store' or file == 'fixed'):
                continue
            f = open(input_dir + '/' + dir + '/' + file,'r+')
            data = f.readlines()
            f.close()
            newlines = []
            for index in final_indexes:
                newlines.append(data[index])
            
            ensure_dir(output_dir + '/' + dir + '/fixed/')
            f = open(output_dir + '/' + dir + '/fixed/' + file,'w')
            f.seek(0)
            f.write(''.join(newlines))
            f.truncate()
            f.close()

        print 'finished processing {}'.format(dir)

    # make sure that the fixed data is now aligned - all n-best files and transcriptions are in the same length
    conversation_dirs = os.listdir(output_dir)
    for dir in conversation_dirs:
        if(dir == '.DS_Store' or dir == 'fixed' or dir == 'bad'):
            continue
        fixed_files = os.listdir(output_dir + '/' + dir + '/fixed/')
        rows_count = -1
        for file in fixed_files:
            if(file == '.DS_Store' or file == 'fixed' or file == 'bad'):
                continue
            f = open(output_dir + '/' + dir + '/fixed/' + '/' + file,'r+')
            data = f.readlines()
            f.close()
            if(rows_count == -1):
                rows_count = len(data)
            else:
                if(len(data)!=rows_count):
                    print 'fixed files are not even in dir: ' + dir + file
                #else:
                    #print 'fixed files are OK in dir: ' + dir + '/' + file + ' len: ' + str(len(data))

    return

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# break the txt files to sentence chunks where every sentence is in a file by itself
def break_txt_to_sentence_chunks(filename, output_dir):
    print 'started breaking file: ' + filename + ' to: ' + output_dir
    ensure_dir(output_dir)
    with open(filename) as input_file:
        content = input_file.readlines()
    i = 0

    for line in content:
        f = open(output_dir + '/' + str(i) + '.txt', 'w')
        if line:
             f.write(line+'\n')
        f.close()
        i = i+1

# convert the manual transcriptions csv files into a txt file
def parse_csv_to_txt():
    conversation_dirs = os.listdir(ROOT_DATA_DIR)
    for dir in conversation_dirs:
        if(dir=='.DS_Store' or dir=='readme_data.txt'):
            continue
            
        print 'parsing transcription csv in ' + dir
        
        # convert to csv if theres only xls
        if(not os.path.isfile(ROOT_DATA_DIR + '/' + dir + '/trans.csv')):
            xls_2_csv(ROOT_DATA_DIR + '/' + dir + '/trans.xls',ROOT_DATA_DIR + '/' + dir + '/trans.csv')
        
        manual_transcripts = []
        
        # open and parse the csv file
        with open(ROOT_DATA_DIR + '/' + dir + '/trans.csv', 'rb') as f:
            reader = csv.reader(f)
            parsed_csv = list(reader)
            #print len(parsed_csv)
            #for line in parsed_csv[1:]:
            #    print len(line)
            #TODO: find out why index out of range is thrown
            try:
                i=0
                for item in parsed_csv[1:]:
                    if(len(item) > 1):
                        manual_transcripts.append(item[1].replace('"','').strip())
                    else:
                        manual_transcripts.append('')
                        print 'error in index: ' + str(i) + ' item: ' + str(item) + ' len: ' + str(len(item))
                    i = i+1
                #manual_transcripts = [ item[1] for item in parsed_csv[1:] ]
            except:
                print 'other error in ' + dir
                #for item in parsed_csv:
                #    print len(item)
            
        # write the csv data to a txt file
        current_output_dir = ROOT_OUTPUT_DIR + '/txts/' + dir + '/txts'
        ensure_dir(current_output_dir)
        f = open(current_output_dir + '/trans.txt', 'w')
        f.write("\n".join(manual_transcripts))
        f.close()
    return
    
# extract the nbest lists from the xml files to a distinct txt file for every n from 1 up to max_n_best_index
def parse_nbest_to_txt(max_n_best_index):
    
    conversation_dirs = os.listdir(ROOT_DATA_DIR)
    print 'found the following xml file dirs {}'.format(conversation_dirs)
    for n_best_index in xrange(1,max_n_best_index+1):
        
        for current_input_dir in conversation_dirs:
            if(current_input_dir=='.DS_Store' or current_input_dir=='readme_data.txt'):
                continue

            # open a directory in the output folder
            current_output_dir = ROOT_OUTPUT_DIR + '/txts/' + current_input_dir
            ensure_dir(current_output_dir)
            print 'parsing {}-best lists to {}'.format(n_best_index, current_output_dir)

            # open a txt file for the n-best-list
            f = open(current_output_dir + '/' + str(n_best_index) + '_best.txt', 'w')
        
            # open every xml file in dir
            files = os.listdir(ROOT_DATA_DIR + '/' + current_input_dir)
            sort_nicely(files)
            for file in files:
                if(file.endswith('.xml')):
                    path = ROOT_DATA_DIR + '/' + current_input_dir + '/' + file
                    #print path
        
                    try:
                        root = ElementTree.parse(path).getroot()
        
                        # get every n_best_index-1 sentence element in the file
                        res = root.findall('result')[0]
                        best = res.findall('hypo')[n_best_index - 1]
        
                        # concat the words into a sentence
                        sentence = " ".join([word.text for word in best.findall('w')])
        
                    except Exception as e:# IndexError, ElementTree.ParseError:
                        print 'could not parse ' + str(n_best_index) + '-best sentence from file ' + path
                        print e
                        # no sentence is found
                        sentence = ''
        
                    # print the sentence into the file
                    f.write(sentence + '\n')
                    #print sentence
            f.close()
    return

# sort files naturally
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

# transform an xls file to a csv file
def xls_2_csv(xls_file_name,csv_file_name):
    
    print >>sys.stderr, 'extracting data from', xls_file_name
    for sheet_name, values in parse_xls(xls_file_name, 'cp1251'): # parse_xls(arg) -- default encoding
        matrix = [[]]
        print 'Sheet = "%s"' % sheet_name.encode('cp866', 'backslashreplace')
        print '----------------'
        for row_idx, col_idx in sorted(values.keys()):
            v = values[(row_idx, col_idx)]
            if isinstance(v, unicode):
                v = v.encode('cp866', 'backslashreplace')
            else:
                v = `v`
            v = '"%s"' % v.strip()
            last_row, last_col = len(matrix), len(matrix[-1])
            while last_row <= row_idx:
                matrix.extend([[]])
                last_row = len(matrix)
    
            while last_col < col_idx:
                matrix[-1].extend([''])
                last_col = len(matrix[-1])
    
            matrix[-1].extend([v])

            # create csv rows
            csv_rows = [', '.join(row) for row in matrix]
            
            # write csv rows
            f = open(csv_file_name, 'w')
            f.write("\n".join(csv_rows))
            f.close()
            
        
    
if __name__ == '__main__':
    main()