"""CodeAnalytics Analyzer

A set of tools to gather metrics about code repositories, files, or 
individual lines that can be used to compare code projects.

Notes
--------------------------------------------------------------------------
    caanalyzer can be run as a program to analyze the current directory.
"""

from cadistributor import log
from .analyzer import Repo, File, Line
from .__main__ import analyze

__version__ = "0.0.6"
