# Markov process solver

## How to run
``` bash
> python3 mdp.py -h                                                                                                                                                         2812
usage: mdp.py [-h] [-df DF] [-min] [-tol TOL] [-iter ITER] [-v] input-file

positional arguments:
  input-file  Specify a input file to read

options:
  -h, --help  show this help message and exit
  -df DF      a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set
  -min        minimize values as costs, defaults to False which maximizes values as rewards
  -tol TOL    a float tolerance for exiting value iteration, defaults to 0.01
  -iter ITER  an integer that indicates a cutoff for value iteration, defaults to 100
  -v          Indicates verbose mode, default to False
```

## Example
``` bash
> python3 mdp.py -df=0.9 -tol=0.001 student2.txt                                                                                                                            2815
Class1 -> Study1
Class2 -> Study2
Class3 -> Pass
Internet -> Class1
Class1=2.647 Class2=5.490 Class3=9.000 Drink=5.693 FB=1.144 Internet=2.382 Pass=10.000 Pub=6.124 Sleep=0.000 Study1=2.941 Study2=6.100
```
