from caanalyzer.analyzer import Analyzer
from sys import argv

def main():
    the_thing = Analyzer(output_raw=False)
    output = the_thing.analyze(argv[1], argv[2])

if __name__ == "__main__":
    main()
