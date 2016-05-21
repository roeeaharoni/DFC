def main():

    input = '/Users/roeeaharoni/research_data/icri-speech/rockin/rockin_audiofiles1.2/Robocup/transcriptions'
    output = '/Users/roeeaharoni/research_data/icri-speech/extracted-data/rockin/ASR-50Best/txts/Robocup/trans.txt'
    with open(input) as input_file:
        lines = input_file.readlines()
        splitted = [l.split('\t')[1] for l in lines if len(l.split('\t'))>1]
        with open(output, 'w') as output_file:
            output_file.writelines(splitted)

if __name__ == '__main__':
    main()