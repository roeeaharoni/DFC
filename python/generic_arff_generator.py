#!/Users/roeeaharoni/anaconda/bin/python

"""
This script creates arff files containing POS, parse tree and word based features out of text files
"""
import os
import sys
import string
import random
import arff
import fileinput
import nltk
from nltk.util import ngrams
import re
from collections import defaultdict
from math import exp
from xml.dom import minidom
#from weka.classifiers import Classifier
from pyparsing import nestedExpr
import sexprs

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# the max ngram length to write as feature name, otherwise name written as 'too long'
MAX_NGRAM_LEN = 30

# the word ngram size
NGRAM_SIZE = 1

# the POS ngram size
POS_NGRAM_SIZE = 1

# the amount of sentences to use from each directory
INSTANCE_AMOUNT = 40000

# the amount of sentences to use from the reference class
REF_INSTANCE_AMOUNT = 40000

# determine whether we use counts or binary features
CREATE_BINARY_FEATURES = True

# defines the sparseness threshold
MIN_SPARSE_THRESHOLD = 30

# determines where the POS annotated data is taken from
POS_DATA_PATH = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/annotations/'

# determines where the parsed annotated data is taken from
PARSE_DATA_PATH = '/Users/roeeaharoni/research_data/icri-speech/ICSI-transcripts/txts/Bed015/parsed/'

# BTW, the weka automator eclipse workspace is /Users/roeeaharoni/Dropbox/master/thesis/code/
def main(args): 
    
    # each directory path is a key to its classification attribute value
    # each directory containing the data for the instances (the sentences)
    input_directories_to_classes = {

    # speech data
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/1_best.txt':'1-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/2_best.txt':'2-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/3_best.txt':'3-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/4_best.txt':'4-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/5_best.txt':'5-best',

    #'/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/0_WER_cluster_0.166.txt':'ASR',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/1_WER_cluster_0.421.txt':'2-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/2_WER_cluster_0.654.txt':'3-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/3_WER_cluster_0.987.txt':'4-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/4_WER_cluster_1.257.txt':'5-best-WER'

    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/0_WER_cluster_0.03428.txt': '1-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/1_WER_cluster_0.14935.txt': '2-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/2_WER_cluster_0.23700.txt': '3-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/3_WER_cluster_0.38376.txt': '4-best-WER',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/4_WER_cluster_0.91128.txt': '5-best-WER'

    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/2_best.txt':'2-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/3_best.txt':'3-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/1_best.txt':'1-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/4_best.txt':'4-best',
    # '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/5_best.txt':'5-best'

        '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/sentence_chunks/1_best.txt':'1-best',
        '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/sentence_chunks/2_best.txt':'2-best',
        '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/sentence_chunks/3_best.txt':'3-best',
        '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/sentence_chunks/4_best.txt':'4-best',
        '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/sentence_chunks/5_best.txt':'5-best'
    }
    
    # speech ref
    ref_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/NAIST/fixed/sentence_chunks/trans.txt'
    # ref_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Robocup/sentence_chunks/trans.txt'
    # ref_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Robocup_Rockin_merged/sentence_chunks/trans.txt'
    # ref_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/merged/sentence_chunks/trans.txt'
    # ref_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/trans.txt'
    ref_label = 'trans'
    
    # output dir name
    dirname = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/arff/NAIST/\
NAIST_nbest_clusters_vs_references_{0}_vs._{1}_{2}_unigram_t{3}_arff/'.format(str(INSTANCE_AMOUNT),
                                                                    str(REF_INSTANCE_AMOUNT),
                                                                    ref_label,
                                                                    str(MIN_SPARSE_THRESHOLD))

    # test_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/0_WER_cluster_0.03428.txt'
    # test_dir = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/WER_clusters/sentence_chunks/1_WER_cluster_0.14935.txt'
    # test_dir = [
    #     '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/1_best.txt',
    #     '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/2_best.txt',
    #     '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/3_best.txt',
    #     '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/4_best.txt',
    #     '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/5_best.txt',
    #     '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/sentence_chunks/trans.txt',
    #     ]

    # create arff file for every path in input_directories_to_classes, using instances from ref_dir
    for path in input_directories_to_classes:
        directories_to_classes = {path:input_directories_to_classes[path], ref_dir:ref_label}
        generate_arff_file(directories_to_classes, dirname) #, test_dir=test_dir, test_label='ASR')
    return

def generate_arff_file(directories_to_classes, output_dir_name, test_dir = False, test_label = False):

    # format the arff file name
    arff_file_name = string.join(directories_to_classes.values(),'_') + '_' + str(NGRAM_SIZE) + '_gram_' + str(INSTANCE_AMOUNT) + '_per_class_' + str(REF_INSTANCE_AMOUNT) +  '_per_ref.arff'
    print 'now making ' + arff_file_name +'\n\n\n'
    arff_file_path = output_dir_name + arff_file_name
    attributes = []
    arff_instance_list = []
    directory_to_instances = {}
    
    # a dictionary counting in how many instances the attribute has been observed, in order to remove sparse attributes later
    attribute_nonzero_count = defaultdict(int)
    
    # make sure the output directory exists, if not, create it
    ensure_dir(output_dir_name)
    
    # counters used for printing
    dir_count = 0
    file_count = 0 
    
    # turn every file in the directory into an instance with attributes
    for directory in directories_to_classes.keys():
        
        # open the directory
        os.chdir(directory)
        
        # get the files 
        total_files = len(os.listdir("."))
        instance_amount = INSTANCE_AMOUNT

        attribute_nonzero_count, attributes, directory_to_instances = extract_attributes_from_files_in_dir(
            attribute_nonzero_count, attributes, directory, directory_to_instances, file_count, instance_amount)


    # announce that data collection has finished
    instances_count = sum([len(a) for a in directory_to_instances.values()])
    print 'finished data collection. found ' + str(len(attributes)) + ' attributes, starting to parse and filter over ' + str(instances_count) + ' instances...'
    #attributes = escape_attributess_arff(attributes)                
    #attributes = sorted(attributes)
    all_attributes_count = len(attributes)
    
    # holds the attributes that were actually used in the process
    filtered_attributes = defaultdict(int)
    instance_count = 0
    
    # create the data as the arff expects it
    for directory in directories_to_classes.keys():
        for instance in directory_to_instances[directory]:
            print 'processing instance no. ' + str(instance_count)
            arff_instance = []
            
            # make sure there is a value for every possible attribute, add only attributes that pass the sparsity threshold
            for a in attributes:
                if attribute_nonzero_count[a] > MIN_SPARSE_THRESHOLD:
                    arff_instance.append(instance[a])
                    filtered_attributes[a] = 1
            
            # add the classification attribute value
            arff_instance.append(directories_to_classes[directory])
            arff_instance_list.append(arff_instance)
            instance_count += 1
    
    filtered_attributes = filtered_attributes.keys()

    # escape signs weka doesn't like
    escaped_attributes = escape_attributess_arff(filtered_attributes)
    escaped_attributes.append('type')

    # create train arff file
    # only if not creating test file now
    # if not test_dir:
    print 'dumping to train file...'
    arff.dump(arff_file_path, arff_instance_list, relation='class', names=escaped_attributes)
    
    # convert the classification attribute to nominal type instead of string
    with open(arff_file_path.replace('.arff', '_nominal.arff'), "wt") as out:
        for line in open(arff_file_path):
            out.write(line.replace("@attribute type string","@attribute type %s"%'{'+','.join(directories_to_classes.values())+'}'))
    
    # remove the non-nominal arff file
    os.remove(arff_file_path)

    print 'created train arff file in: {}'.format(arff_file_path)

    # if there is a test dir (after train feature extraction)
    if test_dir:
        for td in test_dir:


            # once all features are ready extract the features for the test file
            test_file_count = 0
            test_attributes = []
            test_attribute_nonzero_count = defaultdict(int)
            test_directory_to_instances = {}
            test_arff_instance_list = []

            # open the directory
            os.chdir(td)

            # get the files
            total_files = len(os.listdir("."))
            if total_files > INSTANCE_AMOUNT:
                instance_amount = INSTANCE_AMOUNT
            else:
                instance_amount = total_files

            # extract the test instances and attributes
            test_attribute_nonzero_count, test_attributes, test_directory_to_instances = extract_attributes_from_files_in_dir(
                test_attribute_nonzero_count,
                test_attributes,
                td,
                test_directory_to_instances, test_file_count, instance_amount)

            test_instance_count = 0

            # remove all features from the test instances which doesn't exist in the train files and filter sparse features
            for instance in test_directory_to_instances[td]:
                print 'processing instance no. ' + str(test_instance_count)
                arff_instance = []

                # make sure there is a value for every possible attribute, add only attributes that pass the sparsity
                # threshold and exist in train attributes
                for a in attributes:
                    if attribute_nonzero_count[a] > MIN_SPARSE_THRESHOLD:
                        arff_instance.append(instance[a])

                # add the classification attribute value
                arff_instance.append(test_label)
                test_arff_instance_list.append(arff_instance)
                test_instance_count += 1

            # create arff for the test file
            test_arff_file_name = td.split('/')[-1] + 'test.arff'
            print 'now making ' + test_arff_file_name + '\n\n\n'
            arff_file_path = output_dir_name + test_arff_file_name
            print 'dumping to test file...'
            arff.dump(arff_file_path, test_arff_instance_list, relation='class', names=escaped_attributes)

            # convert the classification attribute to nominal type instead of string
            with open(arff_file_path.replace('.arff', '_nominal.arff'), "wt") as out:
                for line in open(arff_file_path):
                    out.write(line.replace("@attribute type string",
                                           "@attribute type %s" % '{' + ','.join(directories_to_classes.values()) + '}'))

            # remove the non-nominal arff file
            os.remove(arff_file_path)
            print 'created test arff file in: {}'.format(arff_file_path)
            print '\nwith {0} attributes ({1} before filtering) and {2} instances'.format(
                str(len(attributes)),
                str(all_attributes_count),
                str(len(test_arff_instance_list)))
    
    # print final message
    print 'created an arff with {0} attributes ({1} before filtering) and {2} instances'.format(str(len(filtered_attributes)),
                                                                                        str(all_attributes_count),
                                                                                        str(len(arff_instance_list)))

    return


# the main feature extraction logic, goes through the files in directory and extracts instances while maintaining a
# global feature type list (attributes)
def extract_attributes_from_files_in_dir(attribute_nonzero_count, attributes, directory, directory_to_instances,
                                         file_count, instance_amount):
    # initialize a list of instances, one instance per file in the directory
    instances = []

    for file in os.listdir(".")[:instance_amount]:
        with open(file, "r") as myfile:
            data = myfile.read()

        # check it is a relevant non-empty txt file
        if file.endswith('.txt') and data:  # and int(file.replace('.txt','')) < INSTANCE_AMOUNT:

            # progress indication
            print str(file) + ' ' + str(file_count) + '/' + str(
                INSTANCE_AMOUNT + REF_INSTANCE_AMOUNT)  # *len(directories_to_classes.keys()))
            file_count += 1

            # generate the word based attributes
            word_attr = defaultdict(int)

            # comment this line to not use word based attributes
            word_attr, attribute_nonzero_count = generate_word_based_attributes(file, attribute_nonzero_count)

            # build the corresponding POS data file path
            pos_data_file_path = POS_DATA_PATH + directory.split('/')[-1] + '/' + file + '.xml'

            # generate the pos based attributes
            pos_attr = defaultdict(int)

            # comment this line to not use POS based attributes
            # pos_attr, attribute_nonzero_count = generate_pos_based_attributes(pos_data_file_path, attribute_nonzero_count)

            # generate the function word based attributes
            fword_attr = defaultdict(int)

            # comment this line to not use function word based attributes
            # fword_attr, attribute_nonzero_count = generate_function_word_based_attributes(file, attribute_nonzero_count)

            # generate the parse-based attributes
            parse_attr = defaultdict(int)

            # format the relevant parse data file path
            parse_data_file_path = PARSE_DATA_PATH + directory.split('/')[-1] + '/' + file

            # comment this line to not use non-terminal parse based attributes
            # parse_attr, attribute_nonzero_count = generate_non_terminal_parse_based_attributes(parse_data_file_path, attribute_nonzero_count)

            # generate the parse-based attributes
            parse_rule_attr = defaultdict(int)

            # comment this line to not use CFG parse based attributes
            # parse_rule_attr, attribute_nonzero_count = generate_CFG_rule_parse_based_attributes(parse_data_file_path, attribute_nonzero_count)

            # generate the unified attribute vector
            instance = defaultdict(int,
                                   word_attr.items() + pos_attr.items() + fword_attr.items() + parse_attr.items() + parse_rule_attr.items())

            # add the file's attribute vector to the list
            instances.append(instance)

            # update the list containing all the possible attributes
            attributes = list(set(attributes + list(instance.keys())))

    # add the instances for the files in the directory
    directory_to_instances[directory] = instances
    return attribute_nonzero_count, attributes, directory_to_instances


# generates an instance consisted of word n-gram attributes
def generate_word_based_attributes(file, attribute_nonzero_count):
    
    # initialize the instance for the file
    hist = defaultdict(int)
    
    # tokenize the data
    with open (file, "r") as myfile:
        data = myfile.read()
        tokens = nltk.word_tokenize(data)
    
    # create ngrams
    ngr = ngrams(tokens, NGRAM_SIZE)
    
    # create attributes
    for s in ngr :
        key = '_'.join(s)
        if CREATE_BINARY_FEATURES:
            hist[key] = 1
        else:
            hist[key] += 1
            
        attribute_nonzero_count[key] += 1
    
    return hist, attribute_nonzero_count

# generates an instance consisted of function word n-gram attributes
def generate_function_word_based_attributes(file, attribute_nonzero_count):
    
    # initialize the instance for the file
    hist = defaultdict(int)
    fwords = []
    fwords_dict = defaultdict(int)
    
    # read the function words from the file
    with open ('/Users/roeeaharoni/research_data/pre_ACL2014/English_Function_Words_Set/moshe.txt', "r") as myfile:
        data = myfile.read()
        fwords = nltk.word_tokenize(data)
    
    max_ngram_len = 0
    for line in fwords:
        if len(line) > max_ngram_len:
            max_ngram_len = len(line)
    
    # tokenize the data
    with open (file, "r") as myfile:
        data = myfile.read().lower()
        tokens = nltk.word_tokenize(data)
    
    # create ngrams
    ngr = ngrams(tokens, 1)
    fwords = ngrams(fwords, 1)
    
    # create attributes
    for s in ngr :
        key = '_'.join(s)
        if CREATE_BINARY_FEATURES:
            hist[key] = 1
        else:
            hist[key] += 1

    #print fwords
    #print ngrams
    for word in fwords:
        key = '_'.join(word)
        if hist[key] == 1:
            if CREATE_BINARY_FEATURES:
                fwords_dict[key] = 1
            else:
                fwords_dict[key] += 1
            attribute_nonzero_count[key] += 1
        else:
            fwords_dict[key] = 0
    
    return fwords_dict, attribute_nonzero_count


# genrates an instance consisted of POS n-gram attributes
def generate_pos_based_attributes(file, attribute_nonzero_count):
    
    # initialize the instance for the file
    pos_attr = defaultdict(int)
    
    # parse every pos in the xml
    xmldoc = minidom.parse(file)
    itemlist = xmldoc.getElementsByTagName('POS')
    
    # create bigrams of POS
    ngr = ngrams(itemlist, POS_NGRAM_SIZE)
    
    # build the instance for the file
    for s in ngr :
        key = '_'.join([item.firstChild.nodeValue for item in s])
        if CREATE_BINARY_FEATURES:
            pos_attr[key] = 1
        else:
            pos_attr[key] += 1
        attribute_nonzero_count[key] += 1
        
    return pos_attr, attribute_nonzero_count
    

def generate_non_terminal_parse_based_attributes(file, attribute_nonzero_count):
    
    # the dictionary to hold the attributes
    parse_attr = defaultdict(int)
    
    # open the parse result file
    with open (file, "r") as myfile:
        parse_data = myfile.read()
        pattern = '\(([A-Z][A-Z]*) '
        matches = re.findall(pattern, parse_data)
        
        for non_terminal in matches:
            key = 'p_' + non_terminal
            if CREATE_BINARY_FEATURES:
                parse_attr[key] = 1
            else:
                parse_attr[key] += 1
            attribute_nonzero_count[key] += 1
        
    return parse_attr, attribute_nonzero_count
    
def generate_CFG_rule_parse_based_attributes(file, attribute_nonzero_count):
    
    # the dictionary to hold the attributes
    parse_CFG_attr = defaultdict(int)
    
    # open the parse result file
    with open (file, "r") as myfile:
        parse_data = myfile.read()
        
        #try:
        #parsed = nestedExpr('(',')').parseString(parse_data).asList()
        try:
            parsed = sexprs.read(parse_data)
        except Exception as e:
            s = str(e)
            print s
            print 'data: ' + parse_data
            exit()
        #print 'data: ' + parse_data
        #print 'parsed: ' + str(parsed)
        rules = get_CFG_rules(parsed)
        for rule in rules:
            key = 'pr_' + rule
            if CREATE_BINARY_FEATURES:
                parse_CFG_attr[key] = 1
            else:
                parse_CFG_attr[key] += 1
            attribute_nonzero_count[key] += 1
        #except Exception as e:
        #    s = str(e)
        #    print file
        #    print e
        
    return parse_CFG_attr, attribute_nonzero_count

def get_CFG_rules(list):
    rules = []
    for item in list:
        rules += get_CFG_rules_recursive(item)
        
    return rules

def get_CFG_rules_recursive(list):
    rules = []
    if len(list) > 1:
        left_operand = list[0]
        right_operands = []
        for i in xrange(1, len(list)):
            #print list[i]
            if len(list[i]) > 0:
                right_operands.append(list[i][0])
        #print 'left: ' +  str(left_operand)
        if len(right_operands) > 0:
            rules.append(left_operand + '_' + "_".join(right_operands))
        
        for i in xrange(1, len(list)):
            if len(list[i]) > 1 and not type(list[i][1]) == type(''):
                #print 'list[i]: ' + str(list[i])
                #print 'len: ' +  str(len(list[i]))
                rules += get_CFG_rules_recursive(list[i])

    return rules

# escapes signs weka don't like
def escape_attributess_arff(attrs):
    res = []
    count = 0
    for attr in attrs:
        attr = attr.replace('$', 'DOLLAR')
        attr = attr.replace('\'\'', 'APOS')
        attr = attr.replace(',', 'COMMA')
        attr = attr.replace('.', 'DOT')
        attr = attr.replace('!', 'EXCL')
        attr = attr.replace('#', 'NMB')
        attr = attr.replace('%', 'PER')
        attr = str(count) + '_' + re.sub('[^A-Za-z0-9\_]+', '', attr)
        
        #attr = attr.replace(' ', '')
        
        try:
            attr = attr.decode('utf-8')
            attr = attr.encode("ascii", "replace")
            
        except:
            print 'encoding exception in attr no. ' + str(count)
            attr = 'uncoded' + str(count)
        if len(attr) > MAX_NGRAM_LEN:
            print 'too long - attr no. ' + str(count)
            attr = 'too_long_' + str(count)
        res.append(attr)
        count += 1
    return res 

if __name__ == "__main__":
    main(sys.argv)