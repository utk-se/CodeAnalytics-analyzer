from cadistributor import log
# from analyzer import Analyzer
from .analyzer import CodeRepo
from .tokens import MethodTokenizer, FileTokenizer, LineTokenizer, ClassTokenizer, LibraryTokenizer, CommentTokenizer, \
    IdLitOpTokenizer
from caanalyzer.metrics import width, height, num_tokens


def analyze(path):
    repo = CodeRepo(path)
    repo.index([FileTokenizer, LineTokenizer, MethodTokenizer, ClassTokenizer, LibraryTokenizer, CommentTokenizer,
                IdLitOpTokenizer], {
                   'size': len, 'width': width, 'height': height, 'num_tokens': num_tokens})
    return repo.df


if __name__ == "__main__":
    log.info("Running analyze on current directory.")
    df = analyze('..')
    print(df.index.names)
    print(df.index.values)
    print(df.loc['.c'])
    # print(df.head(20))
