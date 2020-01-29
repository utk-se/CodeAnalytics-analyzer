# TODO: replace boilerplate
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codeanalytics-analyzer",
    version="0.0.1",
    author="USER",
    author_email="azh@utk.edu",
    description="To be used in combination with codeanalytics aggregator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/utk-se/CodeAnalytics-analyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)