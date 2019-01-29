#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from random import randrange
from threading import Event


class Context(object):
    def __init__(self):
        self.__queue = Queue()
        self.__completed = Event()

    @property
    def completed(self):
        return self.__completed.is_set() and self.__queue.qsize() == 0

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        # Exit if the producer completed
        if self.completed:
            return None

        # Read from the queue with get_nowait(), so we will get an Empty exception when we read
        # from an empty queue. This will prevent us from blocking after producer completion
        try:
            return self.__queue.get_nowait()
        except Empty:
            # Bail if no value is ready to be read
            return None

    def set_data(self, val):
        self.__queue.put(val)


def consumer(id, context):
    while not context.completed:
        data = context.get_data()
        if data is not None:
            print("Consumer {} got {}".format(id, data))
        # Pause a random amount of time
        time.sleep(randrange(2))
    print("Consumer finished")


def producer(context):
    for i in range(20):
        data = "val-{0}".format(i)
        print("Producer put {}".format(data))
        context.set_data(data)
        # Pause a random amount of time
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    context = Context()
    with ThreadPoolExecutor() as executor:
        # We can launch an arbitrary number of consumer threads
        for i in range(3):
            executor.submit(consumer, i, context, )
        executor.submit(producer, context, )


if __name__ == "__main__":
    main()
