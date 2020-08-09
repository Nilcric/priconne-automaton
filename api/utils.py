from .base import *


def Left(delay=True):
    return Click(35, 275, delay=delay and 2)


def Right(delay=True):
    return Click(925, 275, delay=delay and 2)


def Go(x, delay=True):
    if x > 0:
        return Sequence(*(Right(delay) for _ in range(x)))
    else:
        return Sequence(*(Left(delay) for _ in range(-x)))
