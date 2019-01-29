#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
from threading import Event


class EventWrapper(object):
    def __init__(self, id):
        self.__id = id
        self.__event = Event()

    @property
    def id(self):
        return self.__id

    def set(self):
        self.__event.set()

    def wait(self):
        self.__event.wait()


def waiter(wrapper):
    print("Waiting on id: {}".format(wrapper.id))
    wrapper.wait()
    print("Completed id: {}".format(wrapper.id))


def setter(wrappers):
    for wrapper in wrappers:
        print("Calling set on id: {}".format(wrapper.id))
        wrapper.set()
        time.sleep(randrange(2))


def main():
    with ThreadPoolExecutor() as executor:
        wrappers = []
        for i in range(10):
            wrapper = EventWrapper(i)
            wrappers.append(wrapper)
            executor.submit(waiter, wrapper, )
        executor.submit(setter, wrappers, )


if __name__ == "__main__":
    main()
