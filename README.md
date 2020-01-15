# CodeAnalytics-analyzer

Aiden and Jonathan:

 - Given the path to a repo of code
 - Run analysis for all data points specified in metrics points (look at [lizard](https://github.com/terryyin/lizard))
 - Return results in a file based parseable format


## Dependencies (pip)
To install, type: pip install -r requirements.txt
* lizard
* argparse

## Datapoints being reported:
- the nloc (lines of code without comments),
- CCN (cyclomatic complexity number),
- token count of functions.
- parameter count of functions.