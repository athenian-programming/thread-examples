#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from random import randrange


def consumer(id, queue):
    print("Waiting on id: {}".format(id))
    data = queue.get()
    print("Consumed id: {} got data: {}".format(id, data))


def producer(queue):
    for i in range(10):
        data = "val-{}".format(i)
        print("Producer putting data on queue {}".format(data))
        queue.put(data)
        time.sleep(randrange(2))


def main():
    with ThreadPoolExecutor() as executor:
        queue = Queue()
        for i in range(10):
            executor.submit(consumer, i, queue, )
        executor.submit(producer, queue, )


if __name__ == "__main__":
    main()
