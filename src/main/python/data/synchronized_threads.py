#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Event
from threading import Thread


def print_names(name, my_event, next_event):
    for i in range(10):
        my_event.wait()
        print("{0} says hello {1}".format(name, i))
        my_event.clear()
        next_event.set()


def main():
    event1 = Event()
    event2 = Event()
    event3 = Event()

    # Set one of the events
    event1.set()

    Thread(target=print_names, args=("Bob", event1, event2)).start()
    Thread(target=print_names, args=("Bill", event2, event3)).start()
    Thread(target=print_names, args=("Mary", event3, event1)).start()


if __name__ == "__main__":
    main()
