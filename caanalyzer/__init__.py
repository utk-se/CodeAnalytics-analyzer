
"""CA Analyzer

A program to gather metrics about a single repo that can be used to compare repos.

caanalyzer can be run as a program to analyze the current directory (__main__)

Result data is retrieved via analyzer.Analyzer():analyze()
"""

from cadistributor import log
from .analyzer import Analyzer
from .__main__ import analyze

__version__ = "0.0.1"
