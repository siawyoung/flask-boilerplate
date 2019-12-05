#!/usr/bin/env python

from string import ascii_letters
import random


def random_string(length):
    return "".join([random.choice(ascii_letters) for _ in range(length)])


def random_email():
    return "{}@{}.com".format(random_string(8), random_string(10))
