
from bson.json_util import loads, dumps
from cadistributor import log
from .analyzer import Analyzer

def analyze(path):
    the_thing = Analyzer(output_raw=False)
    output = the_thing.analyze(input_path=path)
    # output = the_thing.analyze(argv[1], argv[2])
    return output

if __name__ == "__main__":
    log.info("Running analyze on current directory.")
    print(dumps(analyze(".")))
