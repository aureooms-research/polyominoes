import sys

DEBUG = True
DEBUG = False

def debug (*x, **y):
    if DEBUG:
        print(*x, file=sys.stderr, **y)
