
from cadistributor import log
from .analyzer import Analyzer

def analyze(path):
    the_thing = Analyzer(output_raw=False)
    the_thing.analyze(input_path=".")
    # output = the_thing.analyze(argv[1], argv[2])

if __name__ == "__main__":
    log.info("Running analyze on current directory.")
