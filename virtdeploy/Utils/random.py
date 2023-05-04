import random


def genRandomInRangeWithout(begin, end, exclude=[]):
    while True:
        num = random.randrange(begin, end)
        if num not in exclude:
            return num
