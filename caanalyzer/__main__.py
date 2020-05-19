
from bson.json_util import loads, dumps
from cadistributor import log
# from analyzer import Analyzer
from .analyzer import CodeRepo
from .tokens import MethodTokenizer, FileTokenizer, LineTokenizer
# from .metrics import Length


def analyze(path):
    # the_thing = Analyzer(output_raw=False)
    # output = the_thing.analyze(input_path=path)
    # output = the_thing.analyze(argv[1], argv[2])
    repo = CodeRepo('.')
    repo.index([FileTokenizer, LineTokenizer, MethodTokenizer], {'len': len})
    # return output
    # get average length of a file


if __name__ == "__main__":
    log.info("Running analyze on current directory.")
    print(dumps(analyze(".")))
