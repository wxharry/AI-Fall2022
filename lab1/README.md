# Lab 1 minimax game tree
## Assignment
Write a program that solves a minimax game tree with alpha-beta pruning.

## Usage
```
usage: minimax.py [-h] [-v] [-ab] {min,max} graph-file

positional arguments:
  {min,max}   Specify whether the root player is min or max
  graph-file  Specify a graph file to read

optional arguments:
  -h, --help  show this help message and exit
  -v          Indicates verbose mode
  -ab         Indicates to use alpha-beta pruning (by default do not do A-B)
```

For example:
```
# to run minimax with alpha-beta pruning on example1, and the root player is max.
python3 minimax.py max example1.txt -v -ab
```

## Reference
[Minimax with Alpha Beta Pruning](https://www.youtube.com/watch?v=zp3VMe0Jpf8)
