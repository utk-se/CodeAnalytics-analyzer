from cadistributor import log
# from analyzer import Analyzer
from .analyzer import CodeRepo
from .tokens import MethodTokenizer, FileTokenizer, LineTokenizer
from caanalyzer.metrics import width, height, num_tokens


def analyze(path):
    repo = CodeRepo(path)
    repo.index([FileTokenizer, LineTokenizer, MethodTokenizer], {
               'size': len, 'width': width, 'height': height, 'num_tokens': num_tokens})
    return repo.df


if __name__ == "__main__":
    log.info("Running analyze on current directory.")
