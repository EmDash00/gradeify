# Gradeify 

A program that processes autograder output for ENGR-E111,
penalizes late submissions by 10 points per day, and takes the 
submission with the most amount of points overall after late penalty.

```
usage: gradeify.py [-h] --due DUE [--dir DIR] files [files ...]

Autograder processer and late penalizer for ENGR-E111 at IU.

positional arguments:
  files              files to process

optional arguments:
  -h, --help         show this help message and exit
  --due DUE, -u DUE  Due date in in Year-Month-Day. E.g. 2022-02-22
  --dir DIR, -d DIR  Output directory
```

Example Usage:

```
./gradeify.py Exercise\ 3\ Program\ IO\ Continued_all_scores.csv --due="2022-02-20"
```
