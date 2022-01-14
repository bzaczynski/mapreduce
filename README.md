Parallel word count with [MapReduce](https://en.wikipedia.org/wiki/MapReduce) implemented in vanilla Python 🐍

---

## Usage

This is a classic example of counting words in one or more files using the MapReduce algorithm.  Run the script with one or more text files to get a word count in JSON format:

```console
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
```

## Performance Benchmark

Download a few books in text format from [Project Gutenberg](https://www.gutenberg.org/) and give the script a spin. By default, it will run multiple workers in parallel, taking advantage of your CPU cores: 

```shell
$ time python wordcount.py file1.txt file2.txt (...) > /dev/null

real    0m1.036s
user    0m1.415s
sys     0m0.130s
```

Note, you can change the number of workers by using the `--workers` or `-w` option:

```shell
$ time python wordcount.py file1.txt file2.txt (...) --workers 1 > /dev/null

real    0m1.470s
user    0m1.395s
sys     0m0.147s
```

## MapReduce Algorithm

### Initial Steps

- Combine multiple files into a stream of lines of text
- Split the stream into the individual lines
- Split each line into words
- Filter out words with non-alphabetic characters
- Normalize words to lower case

### Map

- Turn each line into a list of key-value pairs
- Key is a normalized word
- Value is the word's count initially equal to one

### Shuffle

- Merge the list of all mapped lines into one big list of key-value pairs
- Group the intermediate results by a unique key

### Reduce

- Take grouped results for a given word
- Return the word and the total sum of its intermediate counts
