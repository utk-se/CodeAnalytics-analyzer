"""Analyzes the shape of code within the current directory."""

# from bson.json_util import loads, dumps
from cadistributor import log
# from .analyzer import Repo
from caanalyzer import analyzer
import pprint

def analyze(path, ignorefile=None):
    repo = analyzer.Repo(path, ignorefile, True)
    return repo.export()

if __name__ == "__main__":
    log.info("Running analyzer")
    pp = pprint.PrettyPrinter()
    pp.pprint(analyze("..\.."))
