#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from queue import Empty

from random import randrange


class Context(object):
    def __init__(self, manager):
        self.__queue = manager.Queue()
        self.__completed = manager.Event()

    @property
    def completed(self):
        return self.__completed.is_set() and self.__queue.qsize() == 0

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        try:
            data = self.__queue.get(block=True, timeout=1)
            return data
        except Empty:
            return None

    def set_data(self, val):
        self.__queue.put(val)


def consumer(id, context):
    while not context.completed:
        print("Waiting on id: {}".format(id))
        try:
            data = context.get_data()
            print("Consumer {} got {}".format(id, data))
        except Empty:
            continue
    print("Consumer finished")


def producer(context):
    for i in range(10):
        data = "val-{}".format(i)
        print("Producer put {}".format(data))
        context.set_data(data)
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    with ProcessPoolExecutor() as executor:
        # Create Manager to grab a queue and an event
        manager = Manager()
        context = Context(manager)
        # Can start multiple consumers
        for i in range(1):
            executor.submit(consumer, i, context, )
        executor.submit(producer, context, )


if __name__ == "__main__":
    main()
