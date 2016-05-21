import sys
import math


def main(args):

    n = 5
    cluster_amount = 5
    # output_file_format = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/{}_best.txt'
    # wer_file_format = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/{}_best.txt_WER.txt'
    # WER_cluster_file_format = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Rockin_merged/{0}_WER_cluster_{1:.5f}.txt'
    output_file_format = '/Users/roeeaharoni/research_data/icri-speech/NAIST/txts/NAIST/fixed/{}-best.txt'
    wer_file_format = '/Users/roeeaharoni/research_data/icri-speech/NAIST/txts/NAIST/fixed/{}-best.txt_WER.txt'
    WER_cluster_file_format = '/Users/roeeaharoni/research_data/icri-speech/NAIST/txts/NAIST/fixed/{0}_WER_cluster_{1:.5f}.txt'
    max_WER = -1

    # initialize clusters
    # clusters = {}
    # for i in xrange(cluster_amount+1):
    #     clusters[i] = []

    out2wer = []
    # for every n-best list cut
    for i in xrange(n):
        # open all nbest output files
        with open(output_file_format.format(i+1)) as f:
            content = f.readlines()

        # open all matching WER files
        with open(wer_file_format.format(i+1)) as w:
            wer_lines = w.readlines()
            wer_scores = []
            for l in wer_lines[1:-2]:
                score_parts = l.split(',')
                if len(l.split(',')) == 10:
                    wer = float(score_parts[1])
                    wer_scores.append(wer)
                    if wer > max_WER:
                        max_WER = wer
                else:
                    print 'bad WER line in {}'.format(l)


        # pair them
        if len(content) == len(wer_scores):
            zipped = zip(content, wer_scores)
            out2wer += zipped
        else:
            raise Exception

    # cluster into 5 groups according to WER scores, from 0 to max_WER
    # for sentence, score in out2wer:
    #     try:
            # max WER goes to last cluster
            # clusters[int(math.floor(score*cluster_amount/max_WER))].append((sentence, score))
            # except KeyError as e:
            # print score
            # raise e
    out2wer = sorted(out2wer, key=lambda x: x[1])
    clusters = chunks(out2wer, len(out2wer)/cluster_amount)


    # calculate avg WER in cluster
    for c, cluster in enumerate(clusters):
        cluster_WER_sum = 0
        for sentence,score in cluster:
            cluster_WER_sum += score
        if len(cluster) > 0:
            avg_WER = cluster_WER_sum / len(cluster)
            print 'cluster {} avg WER is {} with {} instances'.format(c, avg_WER, len(cluster))

        # print cluster to file
        with open(WER_cluster_file_format.format(c, avg_WER), mode='w') as output_file:
            output_file.writelines([w for w,s in cluster])

    # run classification experiment on sentence chunks

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


if __name__ == "__main__":
    main(sys.argv)