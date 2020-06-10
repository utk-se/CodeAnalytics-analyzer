"""Analyzes the shape of code within the current directory."""

from bson.json_util import loads, dumps
from cadistributor import log
from .analyzer import Repo
import pprint

def analyze(path, ignorefile=None):
    repo = Repo(path, ignorefile, True)
    return repo.export()

if __name__ == "__main__":
    log.info("Running analyze on current directory.")
    pp = pprint.PrettyPrinter()
    pp.pprint(analyze("."))
