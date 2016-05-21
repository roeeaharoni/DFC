import re
from random import randint



def main():
    with open('/Users/roeeaharoni/research_data/icri-speech/rockin/rockin_audiofiles1.2/Rockin2014_Toulouse/transcriptions') as f:
        content = f.readlines()
        print 'found {} lines in trans file'.format(len(content))
    pairs = {}
    for l in content:
        spl = l.split('\t')
        if len(spl) == 2:
            path, text = spl
        else:
            print spl
            continue
        if not path in pairs:
            pairs[path] = text
        else:
            print 'found dup for {}'.format(path)

            pairs[path + '_dup' + str(randint(0,9))] = text

    print 'now have {} lines in dict'.format(len(pairs))
    sorted = sort_nicely(pairs.keys())
    with open('/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin2014_Toulouse/fixed/trans-fixed.txt','w') as f:
        for s in sorted:
            f.write(pairs[s])

    return

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    return l

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
    return [tryint(c) for c in re.split('([0-9]+)', s)]



if __name__ == '__main__':
    main()