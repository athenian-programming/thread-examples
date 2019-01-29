#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
from threading import Event


def print_names(name, my_event, next_event):
    for i in range(20):
        my_event.wait()
        print("{0} says hello {1}".format(name, i))
        my_event.clear()
        next_event.set()
        time.sleep(randrange(2))


def main():
    event1 = Event()
    event2 = Event()
    event3 = Event()

    # Set one of the events
    event1.set()

    with ThreadPoolExecutor() as executor:
        executor.submit(print_names, "Bob", event1, event2, )
        executor.submit(print_names, "Bill", event2, event3, )
        executor.submit(print_names, "Mary", event3, event1, )


if __name__ == "__main__":
    main()
