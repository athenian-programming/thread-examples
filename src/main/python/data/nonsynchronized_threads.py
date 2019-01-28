#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange


def print_names(name):
    for i in range(10):
        print("{0} says hello {1}".format(name, i))
        time.sleep(randrange(2))


def main():
    with ThreadPoolExecutor(max_workers=3) as e:
        e.submit(print_names, "Bob", )
        e.submit(print_names, "Bill", )
        e.submit(print_names, "Mary", )


if __name__ == "__main__":
    main()
