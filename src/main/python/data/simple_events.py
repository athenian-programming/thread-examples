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


def consumer(wrapper):
    print("Consumer waiting on id: {}".format(wrapper.id))
    wrapper.wait()
    print("Consumer completed id: {}".format(wrapper.id))


def producer(wrappers):
    for wrapper in wrappers:
        print("Producer calling set on id: {}".format(wrapper.id))
        wrapper.set()
        time.sleep(randrange(2))


def main():
    with ThreadPoolExecutor() as e:
        wrappers = []
        for i in range(20):
            wrapper = EventWrapper(i)
            wrappers.append(wrapper)
            e.submit(consumer, wrapper)
        e.submit(producer, wrappers, )


if __name__ == "__main__":
    main()
