from caanalyzer.analyzer import Analyzer
from sys import argv
import caanalyzer.agg as agg


def main():
    the_thing = Analyzer(output_raw=False)
    repo_obj = the_thing.analyze(argv[1])
    aggregated_file_data = agg.scalek(repo_obj['file_objs'], 2)


if __name__ == "__main__":
    main()
