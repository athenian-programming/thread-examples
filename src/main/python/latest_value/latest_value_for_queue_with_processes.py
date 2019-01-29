#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from queue import Empty
from random import randrange


class Context(object):
    def __init__(self, manager):
        self.__lock = manager.Lock()
        # Set the maximum size of the Queue to be 1
        self.__queue = manager.Queue(maxsize=1)
        self.__completed = manager.Event()

    @property
    def completed(self):
        with self.__lock:
            return self.__completed.is_set() and self.__queue.qsize() == 0

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        # Exit if the producer completed
        if self.completed:
            return None

        with self.__lock:
            # Read from the queue with get_nowait(), so we will get an Empty exception when we read
            # from an empty queue. This will prevent us from blocking after producer completion
            try:
                return self.__queue.get_nowait()
            except Empty:
                # Bail if no value is ready to be read
                return None

    def set_data(self, val):
        with self.__lock:
            # The queue will be full if the last item assigned has not already been read
            if self.__queue.full():
                # Empty the queue if item is already present
                discarded = self.__queue.get()
                print("Discarded {}".format(discarded))
            print("Put{}".format(val))
            self.__queue.put(val)


def consumer(context):
    while not context.completed:
        data = context.get_data()
        if data is not None:
            print("Consumed {}".format(data))
        # Pause a random amount of time
        time.sleep(randrange(3))
    print("Consumer finished")


def producer(context):
    for i in range(20):
        data = "image-{0}".format(i)
        context.set_data(data)
        # Pause a random amount of time
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    # Create Manager to grab a queue and an event
    manager = Manager()
    context = Context(manager)
    with ProcessPoolExecutor() as executor:
        executor.submit(consumer, context, )
        executor.submit(producer, context, )


if __name__ == "__main__":
    main()
