"""Analyzes the shape of code within the current directory."""

import sys
sys.path.append('..')
from cadistributor import log
from caanalyzer import analyzer
import pprint

def analyze(path, ignorefile=None):
    repo = analyzer.Repo(path, ignorefile, True)
    return repo.export()

if __name__ == "__main__":
    log.info("Running analyzer")
    analyze(r"../hypha-desktop-develop")
    #analyze(r"../MPI.NET-master")
    #analyze(r"../congestion_benchmark")
    #analyze(r"../data-viz-master")
    #pp = pprint.PrettyPrinter()
    #pp.pprint(analyze(r"../caanalyzer"))
    #pp.pprint(analyze(r"../MPI.NET-master"))
