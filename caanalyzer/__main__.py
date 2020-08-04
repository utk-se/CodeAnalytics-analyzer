"""Analyzes the shape of code within the current directory."""

import sys
import argparse
sys.path.append('..')
from cadistributor import log
from caanalyzer import analyzer
import pprint

def analyze(path, ignorefile=None):
    repo = analyzer.Repo(path, ignorefile, True)
    return repo.export()

def main():
    parser = argparse.ArgumentParser(description="CA-Analyzer")
    parser.add_argument('repopath', metavar='repo', type=str, help="Path to repo to analyze")
    args = parser.parse_args()

    log.info(f"Running analyzer on {args.repopath}")
    pp = pprint.PrettyPrinter()
    pp.pprint(analyze(args.repopath))

if __name__ == "__main__":
    main()
