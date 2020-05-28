from setuptools import setup, find_packages

#from caanalyzer import __version__ as moduleversion

def get_version(rel_path):
    with open(rel_path, 'r') as f:
        for line in f.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CAanalyzer",
    version=get_version("caanalyzer/__init__.py"),
    author="Aiden Rutter/Julian Ball/Jonathan Bryan",
    author_email="azh@utk.edu",
    description="To be used in combination with codeanalytics aggregator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/utk-se/CodeAnalytics-analyzer",
    packages=find_packages(),
    install_requires=[
        "lizard>=1.17.3",
        "esprima>=4.0.1",
        "astpretty>=2.0.0",
        "javac-parser>=1.0.0",
        "pycparser>=2.20",
        "ca-distributor @ git+ssh://git@github.com/utk-se/CodeAnalytics-distributor.git#egg=ca-distributor-0.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
