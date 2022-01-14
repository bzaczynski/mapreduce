"""
Calculate the number of unique words in one or more files.

Usage:
$ python wordcount.py file1.txt [file2.txt (...)] [--workers <num_workers>]
{
    "a": 1981,
    "abide": 2,
    "abiding": 1,
    "abilities": 3,
    "able": 53,
    ⋮
    "youngest": 11,
    "your": 424,
    "yours": 2,
    "yourself": 28,
    "yourselves": 1,
    "youth": 7,
    "youths": 1
}
"""
import argparse
import collections
import fileinput
import itertools
import json
import multiprocessing
from typing import TypeAlias, Iterable

WordCount: TypeAlias = tuple[str, int]
WordCounts: TypeAlias = tuple[str, list[int]]


def main(filenames: list[str], num_workers: int) -> None:
    """Print a histogram of the unique word counts in JSON format."""
    if len(filenames) > 0:
        with fileinput.input(files=filenames, encoding="utf-8") as file:
            histogram = dict(count_words(file, num_workers))
            print(json.dumps(histogram, indent=4, sort_keys=True))


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Count words in file(s)")
    parser.add_argument("-w", "--workers", dest="num_workers", type=int)
    parser.add_argument("filenames", metavar="file", nargs="+")
    return parser.parse_args()


def count_words(file: Iterable[str], num_workers: int) -> list[WordCount]:
    """Return a list of unique word counts in a file."""
    with multiprocessing.Pool(processes=num_workers) as pool:
        return pool.map(reducer, shuffle(pool.map(mapper, file)))


def mapper(line: str) -> list[WordCount]:
    """Return a list of all words with their counts initialized to one.

    Sample output:
    [('little', 1), ('would', 1), ('set', 1), ('me', 1), ('up', 1)]
    """
    return [(word.lower(), 1) for word in line.split() if word.isalpha()]


def shuffle(mapped: list[list[WordCount]]) -> list[WordCounts]:
    """Return a list of unique words with their grouped counts.

    Sample output:
    [
        ('little', [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ('would', [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ('set', [1, 1, 1, 1, 1, 1, 1, 1]),
        ('me', [1]),
        ('up', [1, 1, 1, 1, 1, 1, 1, 1, 1])
    ]
    """
    shuffled = collections.defaultdict(list)
    for word, count in itertools.chain(*mapped):
        shuffled[word].append(count)
    return list(shuffled.items())


def reducer(grouped: WordCounts) -> WordCount:
    """Return a word with its total count.

    Sample output:
    ('little', 167)
    """
    word, counts = grouped
    return word, sum(counts)


if __name__ == "__main__":
    arguments = parse_args()
    main(arguments.filenames, arguments.num_workers)
