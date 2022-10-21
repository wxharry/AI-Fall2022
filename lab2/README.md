# Assignment: Map/Vertex coloring via DPLL
Write a program that takes as input in undirected graph, and produces a min "coloring" of the vertices such that no two adjacent vertices have the same color.

## Usage
```
usage: map_coloring.py [-h] [-v] {2,3,4} input-file

positional arguments:
  {2,3,4}     Indicates the number of colors to solve for. If 2 use R, G; if 3 RGB; 4 RGBY
  input-file  Specify a input file to read

options:
  -h, --help  show this help message and exit
  -v          Indicates verbose mode (go through DPLL assignment process)
```

## Example
``` bash
> python3 map_coloring.py 3 triangle.txt
4 = Red
1 = Blue
2 = Green
3 = Red
5 = Blue
6 = Green
9 = Red
8 = Green
7 = Blue
10 = Blue
```

## Reference
[Davis-Putnam (DPLL) procedure](https://cs.nyu.edu/~davise/ai/dp.txt)