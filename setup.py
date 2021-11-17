# flake8: noqa
# pylint: skip-file

from os import path
from setuptools import setup, find_packages

__version__ = None
exec(open("seg_str/version.py").read())

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
    LONG_DESCRIPTION_TYPE = "text/markdown"

setup(
    name="segment-string",
    version=__version__,
    python_requires=">=3.6",
    packages=find_packages(exclude=["test*"]),
    include_package_data=True,
    package_data={"seg_str": ["enwiki_vocab_min200_freq.json.gz"]},
    zip_safe=False,
    url="https://github.com/christophsk/segment-string",
    download_url="https://github.com/christophsk/segment-string",
    license="MIT",
    author="C Skiscim",
    author_email="",
    description="segment-string: Demo of dynamic programming applied to string segmentation",
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    keywords="string-split, string-segment, dynamic-programming, viterbi",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.9",
    ],
)
