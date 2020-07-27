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
    analyze(r"../cypress-develop")
    #analyze(r"../cypress-develop/packages/driver/src/cypress")
    analyze(r"../hypha-desktop-develop")
    analyze(r"../MERN_APP-master")
    analyze(r"../MPI.NET-master")
    #analyze(r"../MPI.NET-master/Benchmarks/NetPipe")
    analyze(r"../congestion_benchmark")
    analyze(r"../data-viz-master")
    #pp = pprint.PrettyPrinter()
    #pp.pprint(analyze(r"../cypress-develop"))
    #pp.pprint(analyze(r"../cypress-develop/packages/server/test/support/fixtures/projects/e2e/reporters"))
    #pp.pprint(analyze(r"../MPI.NET-master/Benchmarks/NetPipe"))
    #pp.pprint(analyze(r"../hypha-desktop-develop"))
    #pp.pprint(analyze('../MERN_APP-master'))
    #pp.pprint(analyze('../MERN_APP-master/models'))
    #pp.pprint(analyze(r"../caanalyzer"))
    #pp.pprint(analyze(r"../MPI.NET-master"))
