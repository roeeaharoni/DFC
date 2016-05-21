#!/Users/roeeaharoni/anaconda/bin/python
import os
import sys

def main():
    naist_file_path = '/Users/roeeaharoni/research_data/icri-speech/NAIST/kbest.txt'
    refs_file_path = '/Users/roeeaharoni/research_data/icri-speech/NAIST/refs.txt'
    nbest_path_format = '/Users/roeeaharoni/research_data/icri-speech/NAIST/{}-best.txt'
    nbest_max = 5
    nbest = {}

    for i in xrange(nbest_max):
        nbest[i] = []

    # open file
    with open(naist_file_path) as naist_file:
        # read lines
        lines = naist_file.readlines()

    # extract refs
    nbest_counter = 0
    refs = []
    for line in lines:
        # remove '** ' and '<GARBAGE> ' tags, remove filename and REF/<eps> signs
        # print 'line: {}'.format(line)

        # skip emoty lines
        if line == '\n':
            # if not all nbest guesses are available for the previous ref, pad with empty lines
            if nbest_counter < nbest_max:
                print 'now padding for ref: {}\n nbest_max is {} nbest_counter is {}'.format(refs[-1],
                                                                                             nbest_max,
                                                                                             nbest_counter)
                for i in xrange(nbest_max - nbest_counter):
                    nbest[nbest_max - i - 1].append('\n')
            continue

        clean_line = ' '.join(line.replace('** ', '').replace('<GARBAGE> ', '').split(' ')[2:])
        # print 'clean line: {}'.format(clean_line)
        # check if this is a reference line
        if ' REF ' in line:
            refs.append(clean_line)
            nbest_counter = 0
            continue
        else:
            clean_line = ' '.join(clean_line.split(' ')[:-1])+ '\n'
            # print clean_line
            # if there are more than nbest_max hypotheses
            if nbest_counter >= nbest_max:
                continue
            else:
                # extract nbest entry
                nbest[nbest_counter].append(clean_line)
                nbest_counter += 1

    # write refs to file
    with open(refs_file_path,'w') as refs_file:
        refs_file.writelines(refs)

    # write nbest lists to files
    for i in xrange(nbest_max):
        with open(nbest_path_format.format(i+1),'w') as nbest_file:
            nbest_file.writelines(nbest[i])

    # measure WER for the nbest lists
    # cluster to nbest WER clusters
    # measure WER over the clusters
    # perform classification experiments on both cluster types
    return

if __name__ == '__main__':
    main()