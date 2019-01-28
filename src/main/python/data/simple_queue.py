#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from random import randrange


class QueueWrapper(object):
    def __init__(self, id, queue):
        self.__id = id
        self.__queue = queue

    @property
    def id(self):
        return self.__id

    def put(self, data):
        self.__queue.put(data)

    def get(self):
        return self.__queue.get()


def consumer(wrapper):
    print("Waiting on id: {}".format(wrapper.id))
    data = wrapper.get()
    print("Consumed id: {} got data: {}".format(wrapper.id, data))


def producer(queue):
    for i in range(10):
        data = "val-{}".format(i)
        print("Producer putting data on queue {}".format(data))
        queue.put(data)
        time.sleep(randrange(2))


def main():
    with ThreadPoolExecutor() as e:
        queue = Queue()
        for i in range(10):
            wrapper = QueueWrapper(i, queue)
            e.submit(consumer, wrapper)
        e.submit(producer, queue, )


if __name__ == "__main__":
    main()
